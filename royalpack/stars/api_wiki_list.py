from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from royalnet.backpack.tables import *
from ..tables import *


class ApiUserListStar(PageStar):
    path = "/api/wiki/list"

    async def page(self, request: Request) -> JSONResponse:
        async with self.alchemy.session_acm() as session:
            pages: typing.List[WikiPage] = await asyncify(session.query(self.alchemy.get(WikiPage)).all)
        return JSONResponse([page.json_list() for page in pages])
