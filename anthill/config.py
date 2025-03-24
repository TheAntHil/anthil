import dataclasses as dc
import os
from dotenv import load_dotenv


load_dotenv()


@dc.dataclass
class Config:
    host: str
    port: int
    debug: bool


def create_config() -> Config:
    return Config(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG")))
