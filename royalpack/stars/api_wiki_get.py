from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from ..tables import *
import uuid


class ApiWikiGetStar(PageStar):
    path = "/api/wiki/get/{wiki_page_uuid}"

    async def page(self, request: Request) -> JSONResponse:
        wiki_page_uuid_str = request.path_params.get("wiki_page_uuid", "")
        try:
            wiki_page_uuid = uuid.UUID(wiki_page_uuid_str)
        except (ValueError, AttributeError, TypeError):
            return shoot(400, "Invalid wiki_page_uuid")
        async with self.alchemy.session_acm() as session:
            wikipage: WikiPage = await asyncify(session.query(self.alchemy.get(WikiPage)).get, wiki_page_uuid)
            if wikipage is None:
                return shoot(404, "No such page")
            return JSONResponse(wikipage.json_full())
