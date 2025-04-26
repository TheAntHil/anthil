from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, models, schemas
from anthill.repos import scheduleds
from datetime import datetime, UTC
from typing import Any

view = Blueprint('scheduleds', __name__,
                 url_prefix='/api/v1/admin/scheduleds')
logger = logging.getLogger(__name__)


def prepare(data: dict[str, Any]) -> schemas.Scheduled:
    scheduled_id = -1
    job_id = data["job_id"]
    scheduled_at = datetime.now(tz=UTC)
    status = models.ScheduledStatus.SCHEDULED

    return schemas.Scheduled(
        scheduled_id=scheduled_id,
        job_id=job_id,
        scheduled_at=scheduled_at,
        status=status,
        )


def convert(scheduled: models.ScheduledTask) -> dict[str, Any]:
    converted_scheduled = {
            "scheduled_id": scheduled.scheduled_id,
            "job_id": scheduled.job_id,
            "scheduled_at": scheduled.scheduled_at.isoformat(),
            "status": scheduled.status.value,
    }
    return converted_scheduled


@view.route('/', methods=['POST'])
def create_scheduled() -> tuple[Response, int]:
    scheduled_json = request.get_json()
    logger.info(f"Received data: {scheduled_json}")
    try:
        prepared_scheduled = prepare(scheduled_json)
        logger.info(f"Processing result: {scheduled_json}")
        with db.db_session() as session:
            scheduled_repo = scheduleds.ScheduledRepo()
            scheduled = scheduled_repo.add(
                        session,
                        prepared_scheduled.job_id,
                        prepared_scheduled.scheduled_at,
                        prepared_scheduled.status,
                    )
        converted_json = convert(scheduled)
        return jsonify(converted_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.route('/', methods=['GET'])
def get_tasks():
    try:
        with db.db_session() as session:
            repo = scheduleds.ScheduledRepo()
            db_tasks = repo.get_scheduled_tasks(session)
            converted_tasks = [convert(task) for task in db_tasks]
            return jsonify(converted_tasks)
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.post("/<int:task_id>/triggered")
def update_task_status(task_id: int):
    try:
        with db.db_session() as session:
            repo = scheduleds.ScheduledRepo()
            if not repo.get_task_by_id(task_id, session):
                return jsonify({"error": "Task not found"}), 404
            repo.update_status_task(session, task_id)
            logger.info("Task status update")
            return jsonify({}), 204
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
