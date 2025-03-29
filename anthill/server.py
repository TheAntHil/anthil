from flask import Flask, request, jsonify
from datetime import datetime
import logging
from anthill import run_handler, queries, system_handler, job_handler
from anthill.queries import insert_job


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
app = Flask(__name__)


@app.route("/api/v1/srv/runs/", methods=["POST"])
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
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/v1/srv/runs/", methods=["GET"])
def get_runs():
    after = datetime.fromisoformat(request.args.get("after").replace(" ", "+"))
    logger.info(f"Received request, parameters: after={after}")
    try:
        db_runs = queries.get_runs(after)
        converted_runs = [run_handler.convert(run) for run in db_runs]
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
        prepared_system = system_handler.convert_to_obj(system_json)
        logger.info(f"Processing result: {prepared_system}")
        answer = queries.insert_system(prepared_system)
        answer_json = system_handler.convert_to_dict(answer)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/admin/jobs/', methods=['POST'])
def create_job():
    job_json = request.get_json()
    logger.info(f"Received data: {job_json}")
    try:
        prepared_job = job_handler.from_dict(job_json)
        logger.info(f"Processing result: {prepared_job}")
        answer = insert_job(prepared_job)
        answer_json = job_handler.to_dict(answer)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500
