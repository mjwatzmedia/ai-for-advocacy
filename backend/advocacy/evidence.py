import re
from .models import Claim, Synthesis, Source, Status, Action

def canonical(text: str):
    return re.sub(r"\s+", " ", text).strip()

def check_claim(claim: Claim, sources: list[Source]) -> Claim:
    """Strict quotation support, NOT automated semantic/legal verification."""
    result = claim.model_copy(deep=True)
    by_id = {s.id: s for s in sources}
    valid = bool(claim.citations)
    for citation in claim.citations:
        source = by_id.get(citation.source_id)
        valid = valid and bool(source and source.text and source.status == Status.verified
                               and canonical(citation.quote) in canonical(source.text))
    if valid and all(canonical(claim.text) == canonical(c.quote) for c in claim.citations):
        result.status = Status.supported
        result.limitation = "Verbatim passage exists in retrieved official text; interpretation, currency and applicability are not established."
    else:
        result.status = Status.needs
        result.limitation = "Missing/invalid evidence or paraphrase requires human verification; not an established fact."
    return result

def validate_synthesis(synthesis: Synthesis, sources: list[Source]):
    result = synthesis.model_copy(deep=True)
    result.claims = [check_claim(c, sources) for c in result.claims]
    valid_ids = {s.id for s in sources if s.text and s.status == Status.verified}
    for option in result.options:
        option.source_ids = [sid for sid in option.source_ids if sid in valid_ids]
        # Suggested action is never an independently verified procedure.
        option.status = Status.needs
    return result

def fallback(sources: list[Source]):
    return Synthesis(claims=[], options=[
        Action(title="Review the retrieved documents",
               detail="Identify relevant passages and confirm applicability with a qualified person. No legal requirements or deadlines have been established.",
               source_ids=[s.id for s in sources if s.status == Status.verified]),
        Action(title="List questions and request clarification",
               detail="Verify the recipient and reporting/participation process before sending any communication."),
        Action(title="Check for an applicable public-comment opportunity",
               detail="Look for a current official notice, agenda or consultation. Confirm jurisdiction, eligibility, format and deadline. No open opportunity has been established."),
        Action(title="Consider a petition or coordinated request",
               detail="Identify a specific decision and a body that can act. Confirm petition rules and signer privacy. No existing petition has been found or endorsed."),
        Action(title="Prepare a call to the responsible representative",
               detail="Use an official directory to identify the correct office. Verify the contact and who represents your location. No phone number is supplied.")
    ], uncertainty=["AI synthesis is disabled or unavailable. These are generic avenues to investigate, not confirmed available opportunities or researched legal findings."])