from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, models, schemas
from anthill.repos import systems
from datetime import datetime, UTC
from typing import Any

view = Blueprint('systems', __name__, url_prefix='/api/v1/admin/systems')
logger = logging.getLogger(__name__)


def prepare(data: dict[str, Any]) -> schemas.System:
    code = data["code"]
    url = data["url"]
    token = data["token"]
    system_type = data["system_type"]
    system_id = -1

    return schemas.System(
        system_id=system_id,
        code=code,
        url=url,
        token=token,
        system_type=system_type,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC)
    )


def convert(system: models.System) -> dict[str, Any]:
    converted_system = {
        "system_id": system.system_id,
        "code": system.code,
        "url": system.url,
        "token": system.token,
        "system_type": system.system_type,
        "created_at": system.created_at.isoformat(),
        "updated_at": system.updated_at.isoformat()
    }
    return converted_system


@view.route('/', methods=['POST'])
def create_system() -> tuple[Response, int]:
    system_json = request.get_json()
    logger.info(f"Received data: {system_json}")
    try:
        prepared_system = prepare(system_json)
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
            converted_system = convert(system)
            return jsonify(converted_system), 201
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500


@view.get('/<int:system_id>')
def get_system_by_id(system_id: int):
    try:
        with db.db_session() as session:
            system_repo = systems.SystemRepo()
            db_system = system_repo.get_system_by_id(system_id, session)
            if db_system is None:
                return jsonify({"error": "System not found"}), 404
            converted_system = convert(db_system)
            return jsonify(converted_system)
    except Exception as e:
        logger.exception("Error processing request")
        return jsonify({"error": str(e)}), 500
