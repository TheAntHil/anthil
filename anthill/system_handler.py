from __future__ import annotations
import uuid
from typing import Any
from anthill import models, schemas


def convert_to_obj(data: dict[str, Any]) -> schemas.System:
    code = data["code"]
    url = data["url"]
    token = data["token"]
    system_type = data["system_type"]
    system_id = str(uuid.uuid4())

    return schemas.System(
        system_id=system_id,
        code=code,
        url=url,
        token=token,
        system_type=system_type,
    )


def convert_to_dto(system_model: models.System) -> schemas.System:
    return schemas.System(
        system_id=system_model.system_id,
        code=system_model.code,
        url=system_model.url,
        token=system_model.token,
        system_type=system_model.system_type,
        created_at=system_model.created_at,
        updated_at=system_model.updated_at
    )


def convert_to_dict(system: schemas.System) -> dict[str, Any]:
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
