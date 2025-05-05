from flask import Blueprint, request, jsonify, Response
from datetime import datetime, UTC
import logging
from anthill import db, schemas, models
from anthill.repos import runs, jobs
from uuid import UUID, uuid4

view = Blueprint('runs', __name__, url_prefix='/api/v1/srv/runs')
logger = logging.getLogger(__name__)


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
            valided_run = schemas.Run.model_validate(run)
            logger.debug(f"Created run object: {valided_run}")
        return jsonify(valided_run.model_dump(mode="json")), 201

    except ValueError as ve:
        logger.exception("Invalid data received")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.get("/")
def get_runs():
    after_str = request.args.get("after")
    if not after_str:
        return jsonify({"error": "'after' query parameter is required"}), 400
    try:
        after = datetime.fromisoformat(after_str.replace(" ", "+"))
        logger.debug(f"Received request, parameters: after={after}")
        with db.db_session() as session:
            run_repo = runs.RunRepo()
            db_runs = run_repo.get_updates(session, after)
            valided_runs = [schemas.Run.model_validate(run)
                            .model_dump(mode="json") for run in db_runs]
        logger.debug(f"Found {len(valided_runs)} runs.")
        return jsonify(valided_runs)

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
            valided_jobs = [schemas.Job.model_validate(job)
                            .model_dump(mode="json") for job in schedule_jobs]
            logger.debug(f"Found {len(valided_jobs)} jobs for run_id={run_id}")
            return jsonify(valided_jobs), 200
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
