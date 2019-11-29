from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *
from royalnet.backpack.tables import *


class ApiUserListStar(PageStar):
    path = "/api/user/list"
    tables = {User}

    async def page(self, request: Request) -> JSONResponse:
        async with self.alchemy.session_acm() as session:
            users: typing.List[User] = await asyncify(session.query(self.alchemy.get(User)).all)
        return JSONResponse([user.json() for user in users])
