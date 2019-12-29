from starlette.requests import Request
from starlette.responses import *
from royalnet.constellation import *
from royalnet.utils import *


class ApiDiscordCvStar(PageStar):
    path = "/api/discord/cv"

    async def page(self, request: Request) -> JSONResponse:
        response = await self.interface.call_herald_event("discord", "discord_cv")
        return JSONResponse(response)
