from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, schemas
from anthill.repos import dependencies
from datetime import datetime, UTC

view = Blueprint('dependencies', __name__,
                 url_prefix='/api/v1/admin/dependencies')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_dependence() -> tuple[Response, int]:
    try:
        depend_json = request.get_json()
        if not depend_json:
            return jsonify({"error": "Invalid JSON body"}), 400
        depend_data = schemas.DependenceCreate.model_validate(depend_json)
        logger.debug(f"Validated dependence data: {depend_data}")
        
        now = datetime.now(tz=UTC)
        with db.db_session() as session:
            repo = dependencies.DependenceRepo()
            dependence = repo.add(session,
                                  depend_data.completed_job_id,
                                  depend_data.trigger_job_id,
                                  now,
                                  now,
                                  )
        valided_dependence = schemas.Dependence.model_validate(dependence)
        logger.debug(f"Converted dependence: {valided_dependence}")
        return jsonify(valided_dependence.model_dump()), 201

    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
