from flask import Blueprint, request, jsonify
import logging
from anthill import db
from anthill.handler import job_handler
from anthill.repos import jobs

view = Blueprint('jobs', __name__, url_prefix='/api/v1/admin/jobs')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_job():
    job_json = request.get_json()
    logger.info(f"Received data: {job_json}")
    try:
        prepared_job = job_handler.from_dict(job_json)
        logger.info(f"Processing result: {prepared_job}")
        with db.db_session() as session:
            job_repo = jobs.JobRepo()
            job = job_repo.add(
                session,
                prepared_job.system_id,
                prepared_job.code,
                prepared_job.scheduler,
                prepared_job.created_at,
                prepared_job.updated_at,
            )
        answer_json = job_handler.to_dict(job)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
