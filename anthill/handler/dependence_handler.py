import uuid
from typing import Any
from datetime import datetime, UTC

from anthill.models import Dependence
from anthill.schemas import DependenceDTO


def from_dict(data: dict[str, Any]) -> Dependence:

    child_code = data["child_code"]
    parent_code = data["parent_code"]
    parent_scheduler = data["parent_scheduler"]
    dependence_id = uuid.uuid4()

    return Dependence(
        dependence_id=dependence_id,
        child_code=child_code,
        parent_code=parent_code,
        parent_scheduler=parent_scheduler,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )


def to_dict(dependence: Dependence) -> dict[str, Any]:

    converted_dependence = {
        "dependence_id": str(dependence.dependence_id),
        "child_code": dependence.child_code,
        "parent_code": dependence.parent_code,
        "parent_scheduler": dependence.parent_scheduler,
        "created_at": dependence.created_at.isoformat(),
        "updated_at": dependence.updated_at.isoformat(),
    }
    return converted_dependence


def to_dto(dependence_model: Dependence) -> DependenceDTO:
    return DependenceDTO(
        dependence_id=str(dependence_model.dependence_id),
        child_code=dependence_model.child_code,
        parent_code=dependence_model.parent_code,
        parent_scheduler=dependence_model.parent_scheduler,
        created_at=dependence_model.created_at,
        updated_at=dependence_model.updated_at,
    )