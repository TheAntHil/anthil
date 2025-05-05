from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, schemas
from anthill.repos import jobs
from datetime import datetime, UTC

view = Blueprint('jobs', __name__, url_prefix='/api/v1/admin/jobs')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_job() -> tuple[Response, int]:
    try:
        job_json = request.get_json()
        if not job_json:
            return jsonify({"error": "Invalid JSON body"}), 400
        job_data = schemas.JobCreate.model_validate(job_json)
        logger.debug(f"Validated job input: {job_data}")
        now = datetime.now(tz=UTC)
        with db.db_session() as session:
            job_repo = jobs.JobRepo()
            job = job_repo.add(session,
                               job_data.system_id,
                               job_data.code,
                               job_data.scheduler,
                               now,
                               now,
                               )
            valided_job = schemas.Job.model_validate(job)
            logger.debug(f"Created job: {valided_job}")
        return jsonify(valided_job.model_dump()), 201

    except ValueError as ve:
        logger.exception("Invalid job data")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.exception("Error creating job")
        return jsonify({"error": str(e)}), 500


@view.get('/<int:job_id>')
def get_job_by_id(job_id: int):
    try:
        with db.db_session() as session:
            job_repo = jobs.JobRepo()
            db_job = job_repo.get_jobs_by_id(job_id, session)
            if db_job is None:
                return jsonify({"error": "Job not found"}), 404

            valided_job = schemas.Job.model_validate(db_job)
            logger.debug(f"Fetched job: {valided_job}")
            return jsonify(valided_job.model_dump())

    except Exception as e:
        logger.exception("Error fetching job")
        return jsonify({"error": str(e)}), 500


# @view.get('/')
# def compute_jobs_to_schedule():
#     pass
