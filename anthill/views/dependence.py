from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, schemas, models
from anthill.repos import dependencies
from datetime import datetime, UTC
from typing import Any


view = Blueprint('dependencies', __name__,
                 url_prefix='/api/v1/admin/dependencies')
logger = logging.getLogger(__name__)


def prepare(data: dict[str, Any]) -> schemas.Dependence:

    completed_job_id = data["completed_job_id"]
    trigger_job_id = data["trigger_job_id"]
    dependence_id = -1

    return schemas.Dependence(
        dependence_id=dependence_id,
        completed_job_id=completed_job_id,
        trigger_job_id=trigger_job_id,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )


def convert(dependence: models.Dependence) -> dict[str, Any]:

    converted_dependence = {
        "dependence_id": dependence.dependence_id,
        "completed_job_id": dependence.completed_job_id,
        "trigger_job_id": dependence.trigger_job_id,
        "created_at": dependence.created_at.isoformat(),
        "updated_at": dependence.updated_at.isoformat(),
    }
    return converted_dependence


@view.route('/', methods=['POST'])
def create_dependence() -> tuple[Response, int]:
    dependence_json = request.get_json()
    logger.info(f"Received data: {dependence_json}")
    try:
        prepared_dependence = prepare(dependence_json)
        logger.info(f"Processing result: {prepared_dependence}")
        with db.db_session() as session:
            job_repo = dependencies.DependenceRepo()
            dependence = job_repo.add(session,
                                      prepared_dependence.completed_job_id,
                                      prepared_dependence.trigger_job_id,
                                      prepared_dependence.created_at,
                                      prepared_dependence.updated_at)
        convert_depedence = convert(dependence)
        return jsonify(convert_depedence), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
