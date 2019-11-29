from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from royalnet.backpack.tables import *


class ApiUserGetStar(PageStar):
    path = "/api/user/get/{uid_str}"

    async def page(self, request: Request) -> JSONResponse:
        uid_str = request.path_params.get("uid_str", "")
        try:
            uid = int(uid_str)
        except (ValueError, TypeError):
            return shoot(400, "Invalid uid")
        async with self.alchemy.session_acm() as session:
            user: User = await asyncify(session.query(self.alchemy.get(User)).get, uid)
        if user is None:
            return shoot(404, "No such user")
        return JSONResponse(user.json())
