import dataclasses as dc
import os
from dotenv import load_dotenv


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


@dc.dataclass
class DbConfig:
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: int

    @property
    def db_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.db_user}:{self.db_pass}@"
            f"{self.db_host}:{self.db_port}/"
            f"{self.db_name}")


db_config = DbConfig(
    db_name=os.getenv("DB_NAME"),
    db_user=os.getenv("DB_USER"),
    db_pass=os.getenv("DB_PASSWORD"),
    db_host=os.getenv("DB_HOST"),
    db_port=int(os.getenv("DB_PORT")))