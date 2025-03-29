from __future__ import annotations
import uuid
from datetime import datetime, UTC
from typing import Any, Optional
import dataclasses as dc

from anthill.models import JobModel


@dc.dataclass
class Job:
    job_id: str
    system_id: str
    code: str
    scheduler: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Job:
        system_id = data["system_id"]
        code = data["code"]
        scheduler = data["scheduler"]
        job_id = str(uuid.uuid4())

        return Job(
            job_id =job_id,
            system_id=system_id,
            code=code,
            scheduler=scheduler,
        )


    @classmethod
    def to_dict(cls, job: Job) -> dict[str, Any]:
        converted_job = {
            "job_id": job.job_id,
            "system_id": job.system_id,
            "code": job.code,
            "scheduler": job.scheduler,
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat()
        }
        return converted_job


    @classmethod
    def to_dto(cls, job_model: JobModel) -> Job:
        return Job(
            job_id=job_model.job_id,
            system_id=job_model.system_id,
            code=job_model.code,
            scheduler=job_model.scheduler,
            created_at=job_model.created_at,
            updated_at=job_model.updated_at
        )