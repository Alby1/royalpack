# Imports go here!
from .api_user_list import ApiUserListStar
from .api_user_get import ApiUserGetStar
from .api_diario_list import ApiDiarioListStar
from .api_diario_get import ApiDiarioGetStar
from .api_discord_cv import ApiDiscordCvStar
from .api_wiki_get import ApiWikiGetStar
from .api_wiki_list import ApiUserListStar

# Enter the PageStars of your Pack here!
available_page_stars = [
    ApiUserListStar,
    ApiUserGetStar,
    ApiDiarioListStar,
    ApiDiarioGetStar,
    ApiDiscordCvStar,
    ApiWikiGetStar,
    ApiUserListStar,
]

# Enter the ExceptionStars of your Pack here!
available_exception_stars = [

]

# Don't change this, it should automatically generate __all__
__all__ = [star.__name__ for star in [*available_page_stars, *available_exception_stars]]
