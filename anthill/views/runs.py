from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
from anthill import run_handler, queries

runs_blueprint = Blueprint('runs', __name__)
logger = logging.getLogger(__name__)


@runs_blueprint.route("/api/v1/srv/runs/", methods=["POST"])
def create_run():
    run = request.get_json()
    logger.info(f"Received data: {run}")
    try:
        prepared_run = run_handler.process_run(run)
        logger.info(f"Processing result: {prepared_run}")
        queries.insert_run(prepared_run)
        converted_run = run_handler.convert(prepared_run)
        return jsonify(converted_run), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@runs_blueprint.route("/api/v1/srv/runs/", methods=["GET"])
def get_runs():
    after = datetime.fromisoformat(request.args.get("after").replace(" ", "+"))
    logger.info(f"Received request, parameters: after={after}")
    try:
        db_runs = queries.get_runs(after)
        converted_runs = [run_handler.convert(run) for run in db_runs]
        logger.info(f"Filtered and sorted fetched {len(converted_runs)} runs.")
        return jsonify(converted_runs)
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
