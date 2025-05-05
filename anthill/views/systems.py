from flask import Blueprint, request, jsonify, Response
import logging
from anthill import db, schemas
from anthill.repos import systems
from datetime import datetime, UTC

view = Blueprint('systems', __name__, url_prefix='/api/v1/admin/systems')
logger = logging.getLogger(__name__)


@view.route('/', methods=['POST'])
def create_system() -> tuple[Response, int]:
    try:
        system_json = request.get_json()
        if not system_json:
            return jsonify({"error": "Invalid JSON body"}), 400
        system_data = schemas.SystemCreate.model_validate(system_json)
        logger.debug(f"Validated system input: {system_data}")
        now = datetime.now(tz=UTC)
        with db.db_session() as session:
            system_repo = systems.SystemRepo()
            system = system_repo.add(session,
                                     system_data.code,
                                     system_data.url,
                                     system_data.token,
                                     system_data.system_type,
                                     now,
                                     now,
                                     )

            valided_system = schemas.System.model_validate(system)
            logger.debug(f"Created system: {valided_system}")

        return jsonify(valided_system.model_dump(mode="json")), 201

    except ValueError as ve:
        logger.exception("Invalid system data")
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        logger.exception("Error creating system")
        return jsonify({"error": str(e)}), 500


@view.get('/<int:system_id>')
def get_system_by_id(system_id: int):
    try:
        with db.db_session() as session:
            system_repo = systems.SystemRepo()
            db_system = system_repo.get_system_by_id(system_id, session)
            if db_system is None:
                return jsonify({"error": "System not found"}), 404

            valided_system = schemas.System.model_validate(db_system)
            logger.debug(f"Fetched system: {valided_system}")
            return jsonify(valided_system.model_dump(mode="json"))

    except Exception as e:
        logger.exception("Error fetching system")
        return jsonify({"error": str(e)}), 500
