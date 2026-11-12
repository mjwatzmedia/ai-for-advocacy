"""Synthetic HTTP fixture. Never used as the application's normal startup."""
import uvicorn
from advocacy.api import create_app
from advocacy.config import Settings
from advocacy.models import Source, Status
class FixtureRetriever:
    async def fetch_many(self,urls,query=""):
        return [Source(id="src-fictional",url="https://www.tucsonaz.gov/Government/City-Clerks-Office",
            title="Fictional public-participation fixture",publisher="City of Tucson",kind="official",
            status=Status.verified,text="Fictional residents may review the published meeting agenda before commenting.",
            retrieved_at="2026-11-12T15:00:00Z",sha256="b"*64,
            limitations=["SYNTHETIC TEST DATA — not a live opportunity."])]
if __name__=="__main__":
    import sys
    uvicorn.run(create_app(Settings(requests_per_minute=120,cors_origins=f"http://127.0.0.1:{sys.argv[1]}"),FixtureRetriever()),host="127.0.0.1",port=int(sys.argv[1]),access_log=False)
