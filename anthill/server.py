from flask import Flask, request, jsonify
import logging
from anthill import queries, system_handler, job_handler
from anthill.views.runs import runs_blueprint


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8"
)

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.register_blueprint(runs_blueprint)


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
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/admin/jobs/', methods=['POST'])
def create_job():
    job_json = request.get_json()
    logger.info(f"Received data: {job_json}")
    try:
        prepared_job = job_handler.from_dict(job_json)
        logger.info(f"Processing result: {prepared_job}")
        answer = queries.insert_job(prepared_job)
        answer_json = job_handler.to_dict(answer)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
