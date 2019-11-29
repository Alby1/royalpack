from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from ..tables import *


class ApiDiarioGetStar(PageStar):
    path = "/api/diario/get/{diario_id}"

    async def page(self, request: Request) -> JSONResponse:
        diario_id_str = request.path_params.get("diario_id", "")
        try:
            diario_id = int(diario_id_str)
        except (ValueError, TypeError):
            return shoot(400, "Invalid diario_id")
        async with self.alchemy.session_acm() as session:
            entry: Diario = await asyncify(session.query(self.alchemy.get(Diario)).get, diario_id)
            if entry is None:
                return shoot(404, "No such user")
            return JSONResponse(entry.json())
