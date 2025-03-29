import uuid
from datetime import datetime, UTC
from typing import Any, Optional
import dataclasses as dc
from anthill import models


@dc.dataclass
class System:
    system_id: str
    code: str
    url: str
    token: str
    system_type: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


def convert_to_obj(data: dict[str, Any]) -> System:
    code = data["code"]
    url = data["url"]
    token = data["token"]
    system_type = data["system_type"]
    system_id = str(uuid.uuid4())

    return System(
        system_id=system_id,
        code=code,
        url=url,
        token=token,
        system_type=system_type,
    )


def convert_to_dto(system_model: models.System) -> System:
    return System(
        system_id=system_model.system_id,
        code=system_model.code,
        url=system_model.url,
        token=system_model.token,
        system_type=system_model.system_type,
        created_at=system_model.created_at,
        updated_at=system_model.updated_at
    )


def convert_to_dict(system: System) -> dict[str, Any]:
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
