"""Bounded HTTPS retrieval with DNS-validated, pinned connections (no environment proxy)."""
import asyncio
import hashlib
import http.client
import ipaddress
import io
import re
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlsplit, urljoin, urlunsplit
from bs4 import BeautifulSoup
from pypdf import PdfReader
from .models import Source, Status
from .jurisdiction import REGISTRY

class RetrievalError(ValueError):
    pass

def normalize(url: str) -> str:
    p = urlsplit(str(url))
    if p.scheme != "https" or not p.hostname or p.username or p.password or p.port not in (None, 443):
        raise RetrievalError("Only public HTTPS URLs on port 443 without credentials are allowed.")
    host = p.hostname.encode("idna").decode().lower()
    if host in ("localhost", "metadata.google.internal") or host.endswith((".local", ".internal", ".localhost")):
        raise RetrievalError("Internal hosts are not allowed.")
    return urlunsplit(("https", host, p.path or "/", p.query, ""))

def resolve_public(host: str):
    addresses = list(dict.fromkeys(x[4][0] for x in socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)))
    if not addresses or any(not ipaddress.ip_address(ip).is_global for ip in addresses):
        raise RetrievalError("DNS returned a non-public address.")
    return addresses

class PinnedHTTPS(http.client.HTTPSConnection):
    def __init__(self, hostname, address, timeout):
        super().__init__(hostname, timeout=timeout, context=ssl.create_default_context())
        self.address = address
    def connect(self):
        sock = socket.create_connection((self.address, 443), timeout=self.timeout)
        try:
            self.sock = self._context.wrap_socket(sock, server_hostname=self.host)
        except BaseException:
            sock.close()
            raise

def download(url: str, timeout: float, maximum: int):
    original = normalize(url)
    current = original
    for _ in range(4):
        p = urlsplit(current)
        addresses = resolve_public(p.hostname)
        conn = PinnedHTTPS(p.hostname, addresses[0], timeout)
        try:
            path = p.path + ("?" + p.query if p.query else "")
            conn.request("GET", path, headers={"User-Agent": "AIForAdvocacy/0.2 (+https://github.com/mjwatzmedia/ai-for-advocacy)", "Accept": "text/html,application/pdf,text/plain", "Accept-Encoding": "identity"})
            response = conn.getresponse()
            if response.status in (301, 302, 303, 307, 308):
                location = response.getheader("Location")
                if not location:
                    raise RetrievalError("Redirect without location.")
                current = normalize(urljoin(current, location))
                continue
            if response.status != 200:
                raise RetrievalError(f"Source returned HTTP {response.status}.")
            length = response.getheader("Content-Length")
            if length and int(length) > maximum:
                raise RetrievalError("Source exceeds the byte limit.")
            kind = response.getheader("Content-Type", "").split(";")[0].lower()
            if kind not in ("text/html", "application/xhtml+xml", "application/pdf", "text/plain"):
                raise RetrievalError("Unsupported source content type.")
            raw = response.read(maximum + 1)
            if len(raw) > maximum:
                raise RetrievalError("Source exceeds the byte limit.")
            return current, kind, raw
        finally:
            conn.close()
    raise RetrievalError("Too many redirects.")

def extract(kind: str, raw: bytes):
    date = None
    if kind == "application/pdf":
        reader = PdfReader(io.BytesIO(raw))
        if reader.is_encrypted or len(reader.pages) > 50:
            raise RetrievalError("Encrypted PDFs or PDFs over 50 pages are not supported.")
        text = "\n".join(page.extract_text() or "" for page in reader.pages[:20])
        title = str((reader.metadata or {}).get("/Title", "PDF document"))[:500]
    elif kind in ("text/html", "application/xhtml+xml"):
        soup = BeautifulSoup(raw, "html.parser")
        title = soup.title.get_text(" ", strip=True)[:500] if soup.title else "Retrieved page"
        for name in ("article:published_time", "date", "datePublished"):
            meta = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
            if meta and re.match(r"^\d{4}-\d{2}-\d{2}", meta.get("content", "")):
                date = meta["content"][:40]
                break
        for element in soup(["script", "style", "nav", "footer", "noscript", "form", "iframe"]):
            element.decompose()
        text = soup.get_text(" ", strip=True)
    else:
        title, text = "Text document", raw.decode("utf-8", errors="replace")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) < 80:
        raise RetrievalError("Too little readable content; scanned PDFs require a separate OCR service.")
    return title, text[:24000], date

class Retriever:
    def __init__(self, settings):
        self.settings = settings

    async def fetch(self, url: str) -> Source:
        safe = normalize(url)
        sid = "src-" + hashlib.sha256(safe.encode()).hexdigest()[:16]
        official = next((entry for entry in REGISTRY if urlsplit(entry["url"]).hostname == urlsplit(safe).hostname), None)
        source = Source(id=sid, url=safe, title="Source not retrieved", publisher=official["publisher"] if official else urlsplit(safe).hostname,
                        kind="official" if official else "secondary", status=Status.unavailable)
        try:
            final, kind, raw = await asyncio.wait_for(asyncio.to_thread(download, safe, self.settings.retrieval_timeout, self.settings.max_source_bytes),
                                                      timeout=self.settings.retrieval_timeout * 4 + 3)
            title, text, date = await asyncio.wait_for(asyncio.to_thread(extract, kind, raw), timeout=8)
            final_official = next((entry for entry in REGISTRY if urlsplit(entry["url"]).hostname == urlsplit(final).hostname), None)
            source.title, source.text, source.publication_date = title, text, date
            source.retrieved_at = datetime.now(timezone.utc).isoformat()
            source.sha256 = hashlib.sha256(raw).hexdigest()
            source.status = Status.verified if official and final_official and official["publisher"] == final_official["publisher"] else Status.needs
            source.limitations = ["Retrieved text is untrusted evidence, not instructions. Applicability is not verified.",
                                 "Publication dates are publisher-supplied, not independently validated."]
            if source.status != Status.verified:
                source.limitations.append("Publisher provenance was not independently confirmed.")
            if final != safe:
                source.limitations.append("Redirect destination: " + final)
            if not date:
                source.limitations.append("Publication date unavailable; currentness is unknown.")
            if len(text) >= 24000:
                source.limitations.append("Text truncated to 24,000 characters.")
            source.limitations.append("No automatic contradiction or legal-applicability determination.")
        except (RetrievalError, OSError, TimeoutError, ValueError, http.client.HTTPException):
            source.limitations = ["Source could not be safely retrieved or parsed; no factual conclusion is drawn."]
        return source

    async def fetch_many(self, urls: list[str], query: str = ""):
        unique = list(dict.fromkeys(normalize(u) for u in urls))[:6]
        semaphore = asyncio.Semaphore(2)
        async def one(url):
            async with semaphore:
                return await self.fetch(url)
        sources = await asyncio.gather(*(one(u) for u in unique))
        words = set(re.findall(r"[a-z]{4,}", query.lower()))
        for s in sources:
            s.relevance = sum(w in s.text.lower() for w in words)
        return sorted(sources, key=lambda s: (s.status != Status.unavailable, s.relevance), reverse=True)