from flask import Blueprint, request, jsonify
import logging
from anthill import job_handler, queries

view = Blueprint('jobs', __name__, url_prefix='/api/v1/admin/jobs')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
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
