from anthill.server import app
from anthill.config import HOST, PORT, DEBUG


def main():
    app.run(host=HOST, port=PORT, debug=DEBUG)


if __name__ == "__main__":
    main()
