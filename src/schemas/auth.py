from pydantic import BaseModel
from configs.settings import settings


class TokenSettings(BaseModel):
    authjwt_secret_key: str = settings.token_secret_key
    authjwt_algorithm: str = "HS256"
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False
