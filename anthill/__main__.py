from anthill.server import app
from anthill.config import create_config


def main():
    config = create_config()
    app.run(host=config.host, port=config.port, debug=config.debug)


if __name__ == "__main__":
    main()
