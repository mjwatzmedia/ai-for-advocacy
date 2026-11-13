from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field, HttpUrl

class Model(BaseModel):
    model_config = ConfigDict(extra="forbid")

class Status(StrEnum):
    verified = "VERIFIED SOURCE"
    supported = "SUPPORTED CLAIM"
    needs = "NEEDS VERIFICATION"
    unavailable = "UNAVAILABLE"
    conflicting = "CONFLICTING EVIDENCE"

class Issue(Model):
    concern: str = Field(min_length=10, max_length=6000)
    outcome: str = Field(min_length=3, max_length=2000)
    location: str = Field(min_length=2, max_length=200)
    consent_retrieval: bool = False
    consent_ai: bool = False

class Analysis(Model):
    category: str
    jurisdiction: str
    institutions: list[str]
    gaps: list[str]
    safety_guidance: list[str]
    user_report: str

class Source(Model):
    id: str
    url: HttpUrl
    title: str = Field(max_length=500)
    publisher: str
    kind: str
    retrieved_at: str | None = None
    publication_date: str | None = None
    status: Status = Status.needs
    text: str = Field(default="", max_length=24000)
    sha256: str | None = None
    limitations: list[str] = Field(default_factory=list)
    relevance: int = 0

class Citation(Model):
    source_id: str
    quote: str = Field(min_length=20, max_length=1500)

class Claim(Model):
    text: str = Field(min_length=1, max_length=2000)
    citations: list[Citation] = Field(default_factory=list, max_length=5)
    status: Status = Status.needs
    limitation: str = "Applicability and interpretation require human review."

class Institution(Model):
    name: str
    jurisdiction: str
    role: str
    source_ids: list[str]
    status: Status
    limitations: list[str]

class Action(Model):
    title: str = Field(min_length=1, max_length=1000)
    detail: str = Field(max_length=4000)
    source_ids: list[str] = Field(default_factory=list, max_length=10)
    status: Status = Status.needs

class Synthesis(Model):
    claims: list[Claim] = Field(default_factory=list, max_length=15)
    options: list[Action] = Field(default_factory=list, max_length=10)
    uncertainty: list[str] = Field(default_factory=list, max_length=20)

class Research(Model):
    analysis: Analysis
    sources: list[Source]
    synthesis: Synthesis
    institutions: list[Institution]
    metadata: dict[str, str]
    limitations: list[str]

class UrlRequest(Model):
    urls: list[HttpUrl] = Field(min_length=1, max_length=6)
    consent_retrieval: bool = False

class EvidenceRequest(Model):
    issue: Issue
    sources: list[Source] = Field(default_factory=list, max_length=6)
    claims: list[Claim] = Field(default_factory=list, max_length=15)

class DraftRequest(Model):
    concern: str = Field(min_length=1, max_length=6000)
    outcome: str = Field(min_length=1, max_length=2000)
    recipient: str = Field(default="Recipient to be verified", max_length=200)
    notes: str = Field(default="", max_length=4000)
    kind: str = Field(default="information", pattern="^(information|public-comment|petition|call)$")

class ExportRequest(Model):
    research: Research
    notes: str = Field(default="", max_length=6000)
    actions: list[Action] = Field(default_factory=list, max_length=15)
    format: str = Field(default="markdown", pattern="^(markdown|json)$")