from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from anthill import run_handler, db
from anthill.repos import runs

view = Blueprint('runs', __name__, url_prefix='/api/v1/srv/runs')
logger = logging.getLogger(__name__)
session = db.get_session()
run_repo = runs.RunRepo(session)


@view.route("/", methods=["POST"])
def create_run():
    run = request.get_json()
    logger.info(f"Received data: {run}")
    try:
        prepared_run = run_handler.process_run(run)
        logger.info(f"Processing result: {prepared_run}")
        run_repo.insert(prepared_run)
        converted_run = run_handler.convert(prepared_run)
        return jsonify(converted_run), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.route("/", methods=["GET"])
def get_runs():
    after = datetime.fromisoformat(request.args.get("after").replace(" ", "+"))
    logger.info(f"Received request, parameters: after={after}")
    try:
        db_runs = run_repo.get(after)
        converted_runs = [run_handler.convert(run) for run in db_runs]
        logger.info(f"Filtered and sorted fetched {len(converted_runs)} runs.")
        return jsonify(converted_runs)
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
