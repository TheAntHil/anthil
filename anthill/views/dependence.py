from flask import Blueprint, request, jsonify
import logging
from anthill import db
from anthill.handler import dependence_handler
from anthill.repos import dependencies

view = Blueprint('dependencies', __name__, url_prefix='/api/v1/admin/dependencies')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_dependence():
    dependence_json = request.get_json()
    logger.info(f"Received data: {dependence_json}")
    try:
        prepared_dependence = dependence_handler.from_dict(dependence_json)
        logger.info(f"Processing result: {prepared_dependence}")
        with db.get_session() as session:
            job_repo = dependencies.DependenceRepo()
            dependence = job_repo.add(session,
                                      prepared_dependence.completed_job_id,
                                      prepared_dependence.trigger_job_id,
                                      prepared_dependence.created_at,
                                      prepared_dependence.updated_at)
        answer_json = dependence_handler.to_dict(dependence)
        return jsonify(answer_json), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
