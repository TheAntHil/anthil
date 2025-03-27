from anthill.server import app
from anthill.config import create_server_config
from anthill.db import create_tables
from anthill.models import RunModel


def main():
    create_tables()
    config = create_server_config()
    app.run(host=config.host, port=config.port, debug=config.debug)


if __name__ == "__main__":
    main()
