from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, models, schemas
from anthill.repos import scheduleds
from datetime import datetime, UTC

view = Blueprint('scheduleds', __name__,
                 url_prefix='/api/v1/admin/scheduleds')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_scheduled() -> tuple[Response, int]:
    try:
        data_json = request.get_json()
        if not data_json:
            return jsonify({"error": "Invalid JSON body"}), 400
        scheduled_data = schemas.ScheduledCreate.model_validate(data_json)
        logger.debug(f"Validated scheduled task: {scheduled_data}")
        now = datetime.now(tz=UTC)
        with db.db_session() as session:
            repo = scheduleds.ScheduledRepo()
            scheduled = repo.add(session,
                                 scheduled_data.job_id,
                                 now,
                                 models.ScheduledStatus.SCHEDULED,
                                 )
        valided_scheduled = schemas.Scheduled.model_validate(scheduled)
        logger.debug(f"Created scheduled task: {valided_scheduled}")
        return jsonify(valided_scheduled.model_dump()), 201
    except Exception as e:
        logger.exception("Error creating scheduled task")
        return jsonify({"error": str(e)}), 500


@view.route('/', methods=['GET'])
def get_tasks():
    try:
        with db.db_session() as session:
            repo = scheduleds.ScheduledRepo()
            db_tasks = repo.get_scheduled_tasks(session)
            valided_tasks = [schemas.Scheduled.model_validate(task)
                             .model_dump() for task in db_tasks]
            logger.debug(f"Fetched {len(valided_tasks)} scheduled tasks")
            return jsonify(valided_tasks)
    except Exception as e:
        logger.exception("Error fetching scheduled tasks")
        return jsonify({"error": str(e)}), 500


@view.post("/<int:task_id>/triggered")
def update_task_status(task_id: int):
    try:
        with db.db_session() as session:
            repo = scheduleds.ScheduledRepo()
            task = repo.get_task_by_id(task_id, session)
            if not task:
                return jsonify({"error": "Task not found"}), 404
            repo.update_status_task(session, task_id)
            logger.debug(f"Task {task_id} status updated to TRIGGERED")
            return jsonify({}), 204
    except Exception as e:
        logger.exception("Error updating task status")
        return jsonify({"error": str(e)}), 500
