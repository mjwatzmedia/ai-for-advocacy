import json
import socket
import httpx
import pytest
from fastapi.testclient import TestClient
from advocacy.config import Settings
from advocacy.api import create_app
from advocacy.models import Issue, Source, Status, Claim, Citation, Synthesis
from advocacy.engine import Engine
from advocacy.providers import AIProvider, ProviderError
from advocacy.workspace import proposal
from advocacy.evidence import check_claim
from advocacy.retrieval import normalize, resolve_public, extract, RetrievalError
from advocacy.jurisdiction import analyze

HEADERS = {"X-Advocacy-Request": "1"}
ISSUE = {"concern": "Residents want safer street crossings.", "outcome": "Ask about the public process.",
         "location": "Tucson, Arizona", "country": "us", "consent_retrieval": True}
TEXT = "Residents should consult the current public meeting agenda before submitting comments. " * 2
SOURCE = Source(id="src-example",url="https://www.tucsonaz.gov/Government/City-Clerks-Office",
                title="Official meeting information",publisher="City of Tucson",kind="official",
                status=Status.verified,text=TEXT,retrieved_at="2026-11-12T14:00:00Z",sha256="a"*64)

class FakeRetriever:
    def __init__(self): self.calls=[]
    async def fetch_many(self,urls,query=""):
        self.calls.append(urls)
        return [SOURCE.model_copy(deep=True)]

class FakeProvider:
    settings=Settings()
    async def synthesize(self,*args):
        raise ProviderError("No model configured.")

def client(**kwargs):
    return TestClient(create_app(Settings(requests_per_minute=120),FakeRetriever(),FakeProvider(),**kwargs))

def test_root_and_readiness():
    c=client()
    assert c.get("/").status_code==200
    assert "Research avenues" in c.get("/").text
    assert c.get("/ready").json()["ai_configured"] is False

def test_workspace_maps_without_notes_or_drafts():
    result=client().post("/api/workspace",headers=HEADERS,json=ISSUE)
    assert result.status_code==200,result.text
    d=result.json()
    assert d["schemaVersion"]==1
    assert d["sources"][0]["id"]=="src-example"
    assert d["sources"][0]["retrievedAt"]=="2026-11-12"
    assert len(d["options"])>=3
    assert all(o["status"]=="needs-review" for o in d["options"])
    assert "authorityNotes" not in d and "correspondence" not in d

def test_no_retrieval_without_consent():
    r=FakeRetriever()
    c=TestClient(create_app(Settings(),r,FakeProvider()))
    d=c.post("/api/workspace",headers=HEADERS,json={**ISSUE,"consent_retrieval":False}).json()
    assert not r.calls and not d["sources"]

def test_selected_urls_and_generic_us():
    r=FakeRetriever()
    c=TestClient(create_app(Settings(),r,FakeProvider()))
    data={**ISSUE,"location":"Sacramento, California","urls":["https://www.usa.gov/elected-officials"]}
    assert c.post("/api/workspace",headers=HEADERS,json=data).status_code==200
    assert r.calls[0]==data["urls"]
    c.post("/api/workspace",headers=HEADERS,json={**ISSUE,"location":"Sacramento, California"})
    assert "https://www.usa.gov/elected-officials" in r.calls[1]
    # Federal directories do not resolve California or municipal jurisdiction.
    assert analyze(Issue(**{k:v for k,v in data.items() if k not in ("country","urls")})).jurisdiction=="Unresolved jurisdiction"

@pytest.mark.parametrize("kind",["information","public-comment","petition","call"])
def test_campaign_drafts_are_unsent_templates(kind):
    d=client().post("/api/drafts",headers=HEADERS,json={"concern":"Fictional street concern","outcome":"Safer crossing","kind":kind}).json()
    assert d["sent"] is False and "Nothing has been sent" in d["text"] and kind in d["text"]

def test_boundaries():
    c=client()
    assert c.post("/api/workspace",json=ISSUE).status_code==403
    assert c.post("/api/workspace",headers={**HEADERS,"Origin":"https://evil.example"},json=ISSUE).status_code==403
    assert c.post("/api/workspace",headers=HEADERS,json={**ISSUE,"unknown":"extra"}).status_code==422
    assert c.post("/api/workspace",headers=HEADERS,json={**ISSUE,"urls":["https://example.com"]*4}).status_code==422
    assert c.post("/api/workspace",headers={**HEADERS,"content-type":"application/json"},content="x"*240001).status_code==413

def test_remote_requires_token_even_with_forged_local_host():
    app=create_app(Settings(),FakeRetriever(),FakeProvider())
    c=TestClient(app,client=("8.8.8.8",1234))
    assert c.post("/api/workspace",headers={**HEADERS,"host":"localhost:8080"},json=ISSUE).status_code==403
    secured=TestClient(create_app(Settings(api_token="test-only-secret"),FakeRetriever(),FakeProvider()))
    assert secured.post("/api/workspace",headers=HEADERS,json=ISSUE).status_code==401
    assert secured.post("/api/workspace",headers={**HEADERS,"Authorization":"Bearer test-only-secret"},json=ISSUE).status_code==200

@pytest.mark.parametrize("url",["http://example.com","https://localhost","https://metadata.google.internal",
                                    "https://test.internal/x","https://u:p@example.com","https://example.com:22"])
def test_url_boundaries(url):
    with pytest.raises((RetrievalError,ValueError)):normalize(url)

def test_private_dns_rejected(monkeypatch):
    monkeypatch.setattr(socket,"getaddrinfo",lambda *a,**kw:[(None,None,None,None,("127.0.0.1",443))])
    with pytest.raises(RetrievalError):resolve_public("example.com")

def test_html_extraction_removes_script():
    title,text,date=extract("text/html",b'<title>Official notice</title><script>INJECTED</script><p>'+TEXT.encode()+b'</p>')
    assert title=="Official notice" and "INJECTED" not in text

def test_claim_quote_is_not_semantic_verification():
    quote="Residents should consult the current public meeting agenda before submitting comments."
    supported=check_claim(Claim(text=quote,citations=[Citation(source_id=SOURCE.id,quote=quote)]),[SOURCE])
    assert supported.status==Status.supported
    paraphrase=check_claim(Claim(text="A meeting is open tomorrow.",citations=[Citation(source_id=SOURCE.id,quote=quote)]),[SOURCE])
    assert paraphrase.status==Status.needs
    forged=check_claim(Claim(text=quote,citations=[Citation(source_id="missing",quote=quote)]),[SOURCE])
    assert forged.status==Status.needs

@pytest.mark.asyncio
async def test_mocked_provider_json_and_fail_closed():
    settings=Settings(llm_provider="openai",llm_api_key="fake-test-key",llm_model="test-model",
                      llm_calls_per_hour=10,llm_budget_usd_per_hour=1,
                      llm_input_usd_per_million=1,llm_output_usd_per_million=1)
    captured=[]
    def response(request):
        captured.append(json.loads(request.content))
        return httpx.Response(200,json={"choices":[{"finish_reason":"stop","message":{"content":json.dumps({"claims":[],"options":[],"uncertainty":["Insufficient evidence."]})}}]})
    p=AIProvider(settings,httpx.MockTransport(response))
    result=await p.synthesize(Issue(concern=ISSUE["concern"],outcome=ISSUE["outcome"],location=ISSUE["location"]),[SOURCE])
    assert result.uncertainty
    assert captured[0]["response_format"]["type"]=="json_object"
    bad=AIProvider(settings,httpx.MockTransport(lambda r:httpx.Response(200,json={"choices":[{"finish_reason":"stop","message":{"content":'{"unrecognized":"bad"}'}}]})))
    with pytest.raises(ProviderError):
        await bad.synthesize(Issue(concern=ISSUE["concern"],outcome=ISSUE["outcome"],location=ISSUE["location"]),[SOURCE])

@pytest.mark.asyncio
async def test_no_keys_or_budget_no_provider_call():
    with pytest.raises(ProviderError):
        await AIProvider(Settings()).synthesize(Issue(concern=ISSUE["concern"],outcome=ISSUE["outcome"],location=ISSUE["location"]),[])

def test_validation_errors_dont_echo_concern():
    r=client().post("/api/workspace",headers=HEADERS,json={"concern":"PRIVATE EXAMPLE"})
    assert r.status_code==422 and "PRIVATE EXAMPLE" not in r.text
