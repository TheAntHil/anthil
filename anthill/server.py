from flask import Flask, request, jsonify
import logging
from anthill.run_handler import process_run, convert
from datetime import datetime as dt
from anthill.queries import insert_run, get_runs_by_db, insert_system
from anthill.system_handler import convert_to_obj, convert_to_dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/api/v1/srv/runs/", methods=["POST"])
def index():
    run = request.get_json()
    logger.info(f"Received data: {run}")
    try:
        prepared_run = process_run(run)
        logger.info(f"Processing result: {prepared_run}")
        insert_run(prepared_run)
        converted_run = convert(prepared_run)
        return jsonify(converted_run), 201
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/srv/runs/", methods=["GET"])
def get_runs():
    after = dt.fromisoformat(request.args.get("after").replace(" ", "+"))
    sort = request.args.get("orderby")
    logger.info(f"Received request, parameters: after={after}, sort={sort}")
    try:
        db_runs = get_runs_by_db(after, sort)
        converted_runs = [convert(run) for run in db_runs]
        logger.info(f"Filtered and sorted fetched {len(converted_runs)} runs.")
        return jsonify(converted_runs)
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/admin/systems/', methods=['POST'])
def create_system():
    system_json = request.get_json()
    logger.info(f"Received data: {system_json}")
    try:
        prepared_system = convert_to_obj(system_json)
        logger.info(f"Processing result: {prepared_system}")
        answer = insert_system(prepared_system)
        answer_json = convert_to_dict(answer)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500
