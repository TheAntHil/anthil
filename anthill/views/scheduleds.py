from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db
from anthill.handler import scheduled_handler
from anthill.repos import scheduleds

view = Blueprint('scheduleds', __name__,
                 url_prefix='/api/v1/admin/scheduleds')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_scheduled() -> tuple[Response, int]:
    scheduled_json = request.get_json()
    logger.info(f"Received data: {scheduled_json}")
    try:
        prepared_scheduled = scheduled_handler.from_dict(scheduled_json)
        logger.info(f"Processing result: {scheduled_json}")
        with db.db_session() as session:
            scheduled_repo = scheduleds.ScheduledRepo()
            scheduled = scheduled_repo.add(
                        session,
                        prepared_scheduled.job_id,
                        prepared_scheduled.scheduled_at,
                        prepared_scheduled.status,
                    )
        converted_json = scheduled_handler.convert(scheduled)
        return jsonify(converted_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
