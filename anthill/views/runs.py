from flask import Blueprint, request, jsonify, Response
from datetime import datetime
import logging
from anthill import db
from anthill.handler import run_handler, job_handler
from anthill.repos import runs, jobs
from uuid import UUID

view = Blueprint('runs', __name__, url_prefix='/api/v1/srv/runs')
logger = logging.getLogger(__name__)


@view.route("/", methods=["POST"])
def create_run():
    run = request.get_json()
    logger.info(f"Received data: {run}")
    try:
        prepared_run = run_handler.process_run(run)
        logger.info(f"Processing result: {prepared_run}")
        with db.db_session() as session:
            run_repo = runs.RunRepo()
            run = run_repo.add(session,
                               prepared_run.run_id,
                               prepared_run.job_id,
                               prepared_run.externol_status,
                               prepared_run.start_time,
                               prepared_run.created_at,
                               prepared_run.updated_at)
        converted_run = run_handler.convert(run)
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
            converted_runs = [run_handler.convert(run) for run in db_runs]
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
            converted_job = [job_handler.convert(job) for job in schedule_jobs]
            return jsonify(converted_job), 200
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
