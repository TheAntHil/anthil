from .server import app
from .config import create_server_config
from .db import create_tables
from .models import RunModel


def main():
    create_tables()
    config = create_server_config()
    app.run(host=config.host, port=config.port, debug=config.debug)


if __name__ == "__main__":
    main()
