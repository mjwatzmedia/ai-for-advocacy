from .jurisdiction import analyze, plan, map_institutions, LIMITATIONS
from .evidence import fallback
from .models import Research
from .providers import ProviderError

class Engine:
    def __init__(self, retriever, provider):
        self.retriever, self.provider = retriever, provider

    async def research(self, issue, urls=None):
        analysis = analyze(issue)
        sources = []
        limitations = list(LIMITATIONS)
        model = "disabled"
        if not issue.consent_retrieval:
            limitations.append("Retrieval not performed: explicit consent required.")
        elif any(term in issue.concern.lower() for term in ("immediate danger", "being abused", "suspected abuse", "emergency")):
            limitations.append("Urgent safeguarding concern: prioritize official reporting guidance, not automated investigation.")
        else:
            try:
                sources = await self.retriever.fetch_many(urls if urls is not None else [s["url"] for s in plan(issue)], issue.concern + " " + issue.outcome)
            except (ValueError, OSError):
                limitations.append("Retrieval provider failed; no evidence was established.")
        synthesis = fallback(sources)
        if issue.consent_ai and sources and any(s.text for s in sources):
            try:
                synthesis = await self.provider.synthesize(issue, sources)
                model = self.provider.settings.llm_model
            except ProviderError as error:
                limitations.append(str(error))
        else:
            limitations.append("No live AI synthesis was requested or sufficient retrieved content was unavailable.")
        return Research(analysis=analysis, sources=sources, synthesis=synthesis,
                        institutions=map_institutions(issue, sources),
                        metadata={"retrieval": "curated-official-pages-v1 (not general web search)", "model": model,
                                  "claim_check": "strict quotation traceability; no semantic applicability verification"},
                        limitations=limitations)

def draft(request):
    context = (f"My concern (user-reported, not independently verified):\n{request.concern}\n\n"
               f"The outcome I seek:\n{request.outcome}\n\n"
               f"Notes to check before use:\n{request.notes}\n\n")
    kinds = {
        "information": "Please direct me to the responsible office, original documents and current participation process.",
        "public-comment": "I offer this comment for your consideration. Please consider the requested change and explain the available next steps.",
        "petition": "Petition proposal: We request the change described above.\n[Describe the specific decision and who can act.]\n[Add a consent-aware signature process only after checking its rules.]",
        "call": "Hello, my name is [name]. I am calling about the concern below. Is this the appropriate office?\n[If not, ask for the official contact.]\n[Ask how residents can provide input. Record any answer separately.]",
    }
    return (f"DRAFT: {request.kind}\nRecipient: {request.recipient}\n\n" + context + kinds[request.kind] +
            "\n\nReview facts, privacy, recipient, eligibility and procedure before use. "
            "No event, petition, telephone number or deadline has been verified. Nothing has been sent or signed.\n")


def markdown(request):
    research = request.research
    lines = ["# Advocacy Game Plan", "", "## User-reported concern", research.analysis.user_report,
             "", "## Jurisdiction", research.analysis.jurisdiction, "", "## Safety guidance",
             *research.analysis.safety_guidance, "", "## Findings"]
    for claim in research.synthesis.claims:
        lines.extend([f"- [{claim.status}] {claim.text}", f"  Limitation: {claim.limitation}"])
        for c in claim.citations:
            lines.append(f"  Evidence {c.source_id}: {c.quote}")
    lines.extend(["", "## Sources"])
    for s in research.sources:
        lines.extend([f"- [{s.id}] [{s.status}] {s.title}: {s.url}",
                      f"  Publisher: {s.publisher}; retrieved: {s.retrieved_at or 'not retrieved'}; publication: {s.publication_date or 'unknown'}",
                      "  " + "; ".join(s.limitations)])
    lines.extend(["", "## Candidate institutions"])
    for i in research.institutions:
        lines.append(f"- {i.name}: {i.role} [{i.status}]. " + "; ".join(i.limitations))
    lines.extend(["", "## Actions"])
    for a in request.actions or research.synthesis.options:
        lines.append(f"- [ ] {a.title}: {a.detail} [{a.status}]")
    lines.extend(["", "## User notes", request.notes, "", "## Uncertainty and limitations",
                  *research.synthesis.uncertainty, *research.limitations,
                  "", "This export is unencrypted. Review it before sharing. No external actions were taken."])
    return "\n".join(lines) + "\n"