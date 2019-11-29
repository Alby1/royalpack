from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from ..tables import *


class ApiDiarioListStar(PageStar):
    path = "/api/diario/list"

    async def page(self, request: Request) -> JSONResponse:
        page_str = request.query_params.get("page", "0")
        try:
            page = int(page_str)
        except (ValueError, TypeError):
            return shoot(400, "Invalid offset")
        async with self.alchemy.session_acm() as session:
            if page < 0:
                page = -page-1
                entries: typing.List[Diario] = await asyncify(
                    session.query(self.alchemy.get(Diario))
                           .order_by(self.alchemy.get(Diario).diario_id.desc()).limit(500)
                           .offset(page * 500)
                           .all
                )
            else:
                entries: typing.List[Diario] = await asyncify(
                    session.query(self.alchemy.get(Diario))
                           .order_by(self.alchemy.get(Diario).diario_id)
                           .limit(500)
                           .offset(page * 500)
                           .all)
            response = [entry.json() for entry in entries]
        return JSONResponse(response)
