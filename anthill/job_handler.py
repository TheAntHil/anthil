from __future__ import annotations
import uuid
from typing import Any
from anthill import models, schemas
from datetime import datetime, UTC


def from_dict(data: dict[str, Any]) -> schemas.Job:
    system_id = data["system_id"]
    code = data["code"]
    scheduler = data["scheduler"]
    job_id = str(uuid.uuid4())

    return schemas.Job(
        job_id=job_id,
        system_id=system_id,
        code=code,
        scheduler=scheduler,
        created_at=datetime.now(tz=UTC),
        updated_at=datetime.now(tz=UTC),
    )


def to_dict(job: schemas.Job) -> dict[str, Any]:
    converted_job = {
        "job_id": job.job_id,
        "system_id": job.system_id,
        "code": job.code,
        "scheduler": job.scheduler,
        "created_at": job.created_at.isoformat(),
        "updated_at": job.updated_at.isoformat()
    }
    return converted_job


def to_dto(job_model: models.Job) -> schemas.Job:
    return schemas.Job(
        job_id=job_model.job_id,
        system_id=job_model.system_id,
        code=job_model.code,
        scheduler=job_model.scheduler,
        created_at=job_model.created_at,
        updated_at=job_model.updated_at
    )
