from datetime import datetime, UTC
from typing import Any

from anthill import models, schemas


def from_dict(data: dict[str, Any]) -> schemas.Dependence:

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


def to_dict(dependence: schemas.Dependence) -> dict[str, Any]:

    converted_dependence = {
        "dependence_id": dependence.dependence_id,
        "completed_job_id": dependence.completed_job_id,
        "trigger_job_id": dependence.trigger_job_id,
        "created_at": dependence.created_at.isoformat(),
        "updated_at": dependence.updated_at.isoformat(),
    }
    return converted_dependence


def to_dto(dependence_model: models.Dependence) -> schemas.Dependence:
    return schemas.Dependence(
        dependence_id=dependence_model.dependence_id,
        completed_job_id=dependence_model.completed_job_id,
        trigger_job_id=dependence_model.trigger_job_id,
        created_at=dependence_model.created_at,
        updated_at=dependence_model.updated_at,
    )