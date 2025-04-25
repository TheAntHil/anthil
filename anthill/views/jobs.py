from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, models, schemas
from anthill.repos import jobs
from datetime import datetime, UTC
from typing import Any


view = Blueprint('jobs', __name__, url_prefix='/api/v1/admin/jobs')
logger = logging.getLogger(__name__)


def prepare(data: dict[str, Any]) -> schemas.Job:
    system_id = data["system_id"]
    code = data["code"]
    scheduler = data["scheduler"]
    job_id = -1

    return schemas.Job(
        job_id=job_id,
        system_id=system_id,
        code=code,
        scheduler=scheduler,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )


def convert(job: models.Job) -> dict[str, Any]:
    converted_job = {
        "job_id": job.job_id,
        "system_id": job.system_id,
        "code": job.code,
        "scheduler": job.scheduler,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat()
    }
    return converted_job


@view.route('/', methods=['POST'])
def create_job() -> tuple[Response, int]:
    job_json = request.get_json()
    logger.info(f"Received data: {job_json}")
    try:
        prepared_job = prepare(job_json)
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
        converted_job = convert(job)
        return jsonify(converted_job), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.get('/<int:job_id>')
def get_job_by_id(job_id: int):
    try:
        with db.db_session() as session:
            job_repo = jobs.JobRepo()
            db_job = job_repo.get_jobs_by_id(job_id, session)
            if db_job is None:
                return jsonify({"error": "Job not found"}), 404
            converted_job = convert(db_job)
            return jsonify(converted_job)
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


# @view.get('/')
# def compute_jobs_to_schedule():
#     pass
