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


def create_db_url() -> str:
    return (
        f"postgresql+psycopg2://"
        f"{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@"
        f"{os.getenv("DB_HOST")}:{int(os.getenv("DB_PORT"))}/"
        f"{os.getenv("DB_NAME")}")
