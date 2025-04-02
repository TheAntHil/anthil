from flask import Blueprint, request, jsonify
import logging
from anthill import system_handler, queries

view = Blueprint('systems', __name__, url_prefix='/api/v1/admin/systems')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_system():
    system_json = request.get_json()
    logger.info(f"Received data: {system_json}")
    try:
        prepared_system = system_handler.convert_to_obj(system_json)
        logger.info(f"Processing result: {prepared_system}")
        answer = queries.insert_system(prepared_system)
        answer_json = system_handler.convert_to_dict(answer)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
