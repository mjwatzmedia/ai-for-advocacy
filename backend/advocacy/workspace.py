"""Deterministic adapter between validated research and the existing case-file schema."""
from .models import Model, Issue, Research
from pydantic import Field, HttpUrl

class WorkspaceRequest(Issue):
    country: str = Field(default="other", pattern="^(us|other)$")
    urls: list[HttpUrl] = Field(default_factory=list, max_length=3)

def proposal(research: Research):
    sources = []
    ids = {s.id for s in research.sources}
    for s in research.sources:
        sources.append({
            "id": s.id, "title": s.title, "url": str(s.url),
            "type": "Primary / official document" if s.kind == "official" else "Research lead / unknown",
            "notes": f"Retrieval: {s.status}. Publisher: {s.publisher}. " + " ".join(s.limitations),
            "publicationDate": (s.publication_date or "")[:10],
            "retrievedAt": (s.retrieved_at or "")[:10], "documentHash": s.sha256 or "", "passages": []})
    claims = []
    for index, c in enumerate(research.synthesis.claims):
        citation = next((x for x in c.citations if x.source_id in ids), None)
        source = next((s for s in research.sources if citation and s.id == citation.source_id), None)
        claims.append({"id": f"research-claim-{index}", "text": c.text,
            "sourceId": citation.source_id if citation else "", "documentHash": source.sha256 or "" if source else "",
            "passage": citation.quote if citation else "", "locator": "Extracted document text",
            "jurisdiction": research.analysis.jurisdiction, "checkedAt": (source.retrieved_at or "")[:10] if source else "",
            "status": "needs-review", "limitation": f"{c.status}: {c.limitation}"})
    institutions = [{"id": f"research-institution-{index}", "name": i.name,
        "responsibility": i.role + " " + " ".join(i.limitations),
        "sourceIds": [sid for sid in i.source_ids if sid in ids], "status": "needs-review"}
        for index, i in enumerate(research.institutions)]
    options = [{"id": f"research-option-{index}", "title": a.title, "evidence": a.detail,
        "effort": "Choose a manageable step; effort not estimated.", "limitations": "Candidate avenue only. Confirm availability, eligibility, contacts and deadlines.",
        "dependencies": a.source_ids, "status": "needs-review"}
        for index, a in enumerate(research.synthesis.options)]
    actions = [{"id": f"research-action-{index}", "title": a.title[:4000], "date": "",
        "basis": a.detail, "done": False, "owner": "", "dateKind": "unspecified"}
        for index, a in enumerate(research.synthesis.options)]
    overview = ["Research mode: " + research.metadata["retrieval"],
                "AI model: " + research.metadata["model"],
                *research.analysis.gaps, *research.analysis.safety_guidance,
                *research.synthesis.uncertainty, *research.limitations]
    return {"schemaVersion": 1, "sources": sources, "institutions": institutions, "claims": claims,
        "options": options, "actions": actions, "summary": "\n".join(overview),
        "researchQuestions": research.analysis.gaps,
        "limitations": research.limitations, "metadata": research.metadata}
