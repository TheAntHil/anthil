from flask import Blueprint, request, jsonify, Response
from datetime import datetime, UTC
import logging
from anthill import db, schemas, models
from anthill.repos import runs, jobs
from anthill.views import jobs as jobs_view
from uuid import UUID, uuid4
from typing import Any


view = Blueprint('runs', __name__, url_prefix='/api/v1/srv/runs')
logger = logging.getLogger(__name__)


def convert(run: models.Run) -> dict[str, Any]:
    converted_run = {
        "run_id": run.run_id,
        "job_id": run.job_id,
        "external_status": run.external_status,
        "start_time": run.start_time.isoformat(),
        "created_at": run.created_at.isoformat(),
        "updated_at": run.updated_at.isoformat(),
        "status": run.status.value,
    }
    return converted_run


@view.route("/", methods=["POST"])
def create_run() -> tuple[Response, int]:
    try:
        json_run = request.get_json()
        if not json_run:
            return jsonify({"error": "Invalid JSON body"}), 400
        run_data = schemas.RunCreate.model_validate(json_run)
        logger.debug(f"Validated data: {run_data}")
        now = datetime.now(tz=UTC)
        run_uuid = uuid4()
        with db.db_session() as session:
            run_repo = runs.RunRepo()
            run = run_repo.add(session,
                               run_uuid,
                               run_data.job_id,
                               run_data.external_status,
                               run_data.start_time,
                               now,
                               now,
                               models.RunStatus.CREATED,
                               )
            converted_run = convert(run)
            return jsonify(converted_run), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.get("/")
def get_runs():
    after = datetime.fromisoformat(request.args.get("after").replace(" ", "+"))
    logger.info(f"Received request, parameters: after={after}")
    try:
        with db.db_session() as session:
            run_repo = runs.RunRepo()
            db_runs = run_repo.get_updates(session, after)
            converted_runs = [convert(run) for run in db_runs]
            logger.info(f"Quantity in the sample {len(converted_runs)} runs.")
            return jsonify(converted_runs)
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.post("/<uuid:run_id>/schedule")
def compute_jobs_to_schedule(run_id: UUID) -> tuple[Response, int]:
    try:
        with db.db_session() as session:
            jobs_repo = jobs.JobRepo()
            schedule_jobs = jobs_repo.get_schedule_jobs_for_run(run_id,
                                                                session)
            converted_job = [jobs_view.convert(job) for job in schedule_jobs]
            return jsonify(converted_job), 200
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
