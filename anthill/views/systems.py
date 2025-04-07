from flask import Blueprint, request, jsonify
import logging
from anthill import db
from anthill.handler import system_handler
from anthill.repos import systems

view = Blueprint('systems', __name__, url_prefix='/api/v1/admin/systems')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_system():
    system_json = request.get_json()
    logger.info(f"Received data: {system_json}")
    try:
        prepared_system = system_handler.from_dict(system_json)
        logger.info(f"Processing result: {prepared_system}") 
        with db.db_session() as session:
            system_repo = systems.SystemRepo()
            system = system_repo.add(session,
                                     prepared_system.code,
                                     prepared_system.url,
                                     prepared_system.token,
                                     prepared_system.system_type,
                                     prepared_system.created_at,
                                     prepared_system.updated_at)
            answer_json = system_handler.to_dict(system)
            return jsonify(answer_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
