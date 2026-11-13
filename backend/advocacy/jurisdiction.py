import re
from .models import Analysis, Issue, Institution, Source, Status

# Explicitly maintained starting points, not invented search results or proof of applicability.
CIVIC_REGISTRY = [
    {"url": "https://www.usa.gov/elected-officials", "publisher": "USA.gov", "name": "USA.gov official directory", "role": "Starting point to identify elected officials; a specific representative is not yet verified", "category": "general"},
    {"url": "https://www.regulations.gov/", "publisher": "Regulations.gov", "name": "Federal rulemaking portal", "role": "Federal public-comment starting point, not a local process or proof an applicable comment period is open", "category": "general"},
]
REGISTRY = CIVIC_REGISTRY + [
    {"url": "https://www.azleg.gov/ars/13/03620.htm", "publisher": "Arizona Legislature", "name": "Arizona Legislature", "role": "Statutory text; not an individual reporting or enforcement channel", "category": "child safeguarding"},
    {"url": "https://dcs.az.gov/report-child-abuse", "publisher": "Arizona Department of Child Safety", "name": "Arizona Department of Child Safety", "role": "Official child protection reporting information; eligibility and applicability need review", "category": "child safeguarding"},
    {"url": "https://www.azag.gov/complaints", "publisher": "Arizona Attorney General", "name": "Arizona Attorney General", "role": "Complaint directory; confirm the appropriate program", "category": "general"},
    {"url": "https://www.tucsonaz.gov/Government/City-Clerks-Office", "publisher": "City of Tucson", "name": "Tucson City Clerk", "role": "Municipal participation and records starting point", "category": "general"},
    {"url": "https://www.pima.gov/", "publisher": "Pima County", "name": "Pima County government", "role": "County directory; specific responsible office not established", "category": "general"},
]
LIMITATIONS = [
    "Source retrieval verifies provenance, not legal applicability or truth of allegations.",
    "Dates and deadlines are not assumed. Missing publication dates require review.",
    "This service never sends messages, files complaints or makes legal determinations.",
]
def analyze(issue: Issue) -> Analysis:
    text = issue.concern.lower()
    loc = issue.location.lower()
    az = bool(re.search(r"\barizona\b|\baz\b|\btucson\b|\bpima\b", loc))
    child = any(w in text for w in ("child", "children", "youth", "safeguard"))
    urgency = any(w in text for w in ("immediate danger", "emergency", "being abused", "suspected abuse"))
    safety = ["For immediate danger in the United States, contact emergency services (911). Do not use this tool to investigate a child's disclosure."]
    if child:
        safety.append("Use the official child protection reporting page and qualified local guidance for suspected abuse; research is not a substitute for prompt reporting.")
    return Analysis(category="child safeguarding" if child else "general civic issue",
        jurisdiction="Arizona, United States" if az else "Unresolved jurisdiction",
        institutions=["State child protection", "State legislature", "Local government", "Organization governance"] if child and az else ["Institutional authority requires research"],
        gaps=[] if az else ["Confirm the state/country; only the Arizona module is implemented."],
        safety_guidance=safety if child or urgency else [],
        user_report=issue.concern)

def plan(issue: Issue):
    analysis = analyze(issue)
    if analysis.jurisdiction.startswith("Unresolved"):
        return []
    result = [s for s in REGISTRY if s not in CIVIC_REGISTRY and (s["category"] == "general" or analysis.category == "child safeguarding")]
    loc = issue.location.lower()
    return [s for s in result if ("tucsonaz.gov" not in s["url"] or "tucson" in loc)
            and ("pima.gov" not in s["url"] or "pima" in loc or "tucson" in loc)]

def map_institutions(issue: Issue, sources: list[Source]):
    result = []
    for entry in plan(issue):
        found = next((s for s in sources if str(s.url).rstrip("/") == entry["url"].rstrip("/")), None)
        result.append(Institution(name=entry["name"], jurisdiction=analyze(issue).jurisdiction,
            role=entry["role"], source_ids=[found.id] if found else [],
            status=Status.needs,
            limitations=["Directory candidate, not a determination of jurisdiction or authority.",
                          "Review retrieved evidence before contacting."] +
                          ([] if found and found.status == Status.verified else ["Official page has not been successfully retrieved."])))
    return result