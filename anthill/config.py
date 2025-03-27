import dataclasses as dc
import os
from dotenv import load_dotenv
import psycopg2


load_dotenv()


@dc.dataclass
class ServerConfig:
    host: str
    port: int
    debug: bool


def create_server_config() -> ServerConfig:
    return ServerConfig(
        host=os.getenv("HOST"),
        port=int(os.getenv("PORT")),
        debug=bool(os.getenv("DEBUG")))


def get_db_url() -> str:
    return os.getenv("DB_URL")
