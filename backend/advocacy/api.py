import asyncio
from collections import defaultdict, deque
import json
import logging
from pathlib import Path
import secrets
import time
from urllib.parse import urlsplit
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import Settings
from .models import Issue, UrlRequest, EvidenceRequest, DraftRequest, ExportRequest
from .retrieval import Retriever, RetrievalError
from .providers import AIProvider
from .engine import Engine, draft, markdown
from .jurisdiction import analyze, map_institutions, plan, CIVIC_REGISTRY
from .evidence import check_claim, fallback
from .workspace import WorkspaceRequest, proposal

logger = logging.getLogger("advocacy")
ROOT = Path(__file__).resolve().parents[2]

def create_app(settings=None, retriever=None, provider=None):
    s = settings or Settings()
    engine = Engine(retriever or Retriever(s), provider or AIProvider(s))
    app = FastAPI(title="AI for Advocacy research API", version="0.2.0")
    app.state.engine = engine
    app.state.settings = s
    calls = defaultdict(deque)
    concurrency = asyncio.Semaphore(s.max_parallel_research)
    app.add_middleware(CORSMiddleware, allow_origins=s.cors_origins.split(","),
                       allow_methods=["GET", "POST"], allow_headers=["Content-Type", "Authorization", "X-Advocacy-Request"])

    class Boundary:
        def __init__(self, wrapped):
            self.app = wrapped
        async def __call__(self, scope, receive, send):
            if scope["type"] != "http":
                return await self.app(scope, receive, send)
            started = time.monotonic()
            request_id = secrets.token_hex(8)
            headers = dict(scope.get("headers", []))
            path = scope["path"]
            is_api = path.startswith("/api/")
            async def deny(code, reason):
                await JSONResponse({"error": {"code": reason, "message": reason.replace("_", " "),
                                             "request_id": request_id}}, status_code=code)(scope, receive, send)
            if is_api:
                if s.api_token:
                    supplied = headers.get(b"authorization", b"").decode()
                    if not secrets.compare_digest(supplied, "Bearer " + s.api_token):
                        return await deny(401, "authorization_required")
                else:
                    # Default is localhost-only with no credentials. Remote exposure requires token/TLS.
                    try:
                        host = urlsplit("http://" + headers.get(b"host", b"").decode()).hostname
                    except ValueError:
                        host = None
                    if host not in ("localhost", "127.0.0.1", "::1", "testserver") or (scope.get("client") or ("",))[0] not in ("127.0.0.1", "::1", "testclient"):
                        return await deny(403, "local_installation_only")
                origin = headers.get(b"origin", b"").decode()
                if origin and origin not in s.cors_origins.split(","):
                    return await deny(403, "origin_not_allowed")
                if scope["method"] == "POST" and headers.get(b"x-advocacy-request") != b"1":
                    return await deny(403, "request_header_required")
                if scope["method"] == "POST" and not headers.get(b"content-type", b"").startswith(b"application/json"):
                    return await deny(415, "json_required")
                # Bounded rate state; not a database or permanent client log.
                now = time.monotonic()
                key = (scope.get("client") or ("unknown",))[0]
                for stale in list(calls):
                    if not calls[stale] or now - calls[stale][-1] >= 60:
                        del calls[stale]
                if len(calls) > 1024:
                    return await deny(429, "rate_state_full")
                q = calls[key]
                while q and now - q[0] >= 60:
                    q.popleft()
                if len(q) >= s.requests_per_minute:
                    return await deny(429, "rate_limit_reached")
                q.append(now)
            body = bytearray()
            if scope["method"] == "POST":
                try:
                    while True:
                        message = await asyncio.wait_for(receive(), timeout=10)
                        if message["type"] == "http.disconnect":
                            return
                        body.extend(message.get("body", b""))
                        if len(body) > s.max_request_bytes:
                            return await deny(413, "request_too_large")
                        if not message.get("more_body", False):
                            break
                except TimeoutError:
                    return await deny(408, "request_timeout")
            consumed = False
            async def bounded_receive():
                nonlocal consumed
                if not consumed:
                    consumed = True
                    return {"type": "http.request", "body": bytes(body), "more_body": False}
                return await receive()
            async def secure_send(message):
                if message["type"] == "http.response.start":
                    message["headers"] += [
                        (b"cache-control", b"no-store"), (b"x-content-type-options", b"nosniff"),
                        (b"referrer-policy", b"no-referrer"),
                        (b"content-security-policy", b"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'")]
                await send(message)
            try:
                await self.app(scope, bounded_receive if scope["method"] == "POST" else receive, secure_send)
            except Exception:
                await deny(500, "internal_failure")
            finally:
                # No raw URL, query, client IP, request body, prompt, exception or credentials.
                logger.info(json.dumps({"event": "request", "request_id": request_id,
                                        "duration_ms": round((time.monotonic()-started)*1000)}))
    app.add_middleware(Boundary)

    @app.exception_handler(RequestValidationError)
    async def invalid(request, exc):
        return JSONResponse({"error": {"code": "validation_error", "message": "Request does not match the documented schema."}}, status_code=422)

    @app.exception_handler(RetrievalError)
    async def unsafe(request, exc):
        return JSONResponse({"error": {"code": "unsafe_source", "message": "Source URL failed safe-retrieval validation."}}, status_code=400)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.get("/ready")
    def ready():
        return {"status": "ready", "retrieval": "curated official sources; network availability not guaranteed",
                "ai_configured": s.ai_ready(), "live_ai_verified": False, "storage": "none"}

    @app.post("/api/plan")
    async def legacy_plan():
        return JSONResponse({"error": "This research server uses the structured Research advocacy avenues controls above. The legacy free-text generator is not connected here."}, status_code=409)

    @app.post("/api/issues/analyze")
    def issue_analyze(issue: Issue):
        return analyze(issue)

    @app.post("/api/research")
    async def research(issue: Issue):
        async with concurrency:
            return await engine.research(issue)

    @app.post("/api/workspace")
    async def workspace(issue: WorkspaceRequest):
        selected = [str(u) for u in issue.urls]
        if not selected:
            selected = [entry["url"] for entry in plan(issue)]
            if not selected and issue.country == "us":
                selected = [entry["url"] for entry in CIVIC_REGISTRY]
        async with concurrency:
            researched = await engine.research(Issue.model_validate(
                {k: v for k, v in issue.model_dump().items() if k not in ("urls", "country")}), selected)
        return proposal(researched)

    @app.post("/api/sources/verify")
    async def verify(request: UrlRequest):
        if not request.consent_retrieval:
            return JSONResponse({"error": {"code": "consent_required", "message": "Explicit source-retrieval consent is required."}}, status_code=403)
        async with concurrency:
            return await engine.retriever.fetch_many([str(u) for u in request.urls])

    async def refreshed(request: EvidenceRequest):
        if not request.issue.consent_retrieval:
            return []
        # Never accept client supplied text/status as trusted evidence.
        return await engine.retriever.fetch_many([str(x.url) for x in request.sources])

    @app.post("/api/institutions/map")
    async def institutions(request: EvidenceRequest):
        async with concurrency:
            sources = await refreshed(request)
        return map_institutions(request.issue, sources)

    @app.post("/api/roadmap")
    async def roadmap(request: EvidenceRequest):
        async with concurrency:
            sources = await refreshed(request)
        return {"claims": [check_claim(c, sources) for c in request.claims],
                "actions": fallback(sources).options,
                "limitations": ["Procedures, legal applicability and deadlines require review."]}

    @app.post("/api/drafts")
    def drafts(request: DraftRequest):
        return {"text": draft(request), "sent": False, "status": "HUMAN REVIEW REQUIRED"}

    @app.post("/api/export")
    def export(request: ExportRequest):
        if request.format == "json":
            return Response(json.dumps(request.model_dump(mode="json"), indent=2), media_type="application/json",
                            headers={"Content-Disposition": 'attachment; filename="advocacy-workspace.json"'})
        return Response(markdown(request), media_type="text/markdown",
                        headers={"Content-Disposition": 'attachment; filename="advocacy-game-plan.md"'})

    if (ROOT / "public").exists():
        app.mount("/", StaticFiles(directory=ROOT / "public", html=True), name="workspace")
    return app

app = create_app()
