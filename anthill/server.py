from flask import Flask
import logging
from anthill.views.runs import runs
from anthill.views.jobs import jobs
from anthill.views.system import systems


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
app = Flask(__name__)

app.register_blueprint(runs)

app.register_blueprint(jobs)

app.register_blueprint(systems)
