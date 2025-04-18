from datetime import datetime, UTC
from typing import Any
from anthill import models, schemas


def from_dict(data: dict[str, Any]) -> schemas.Scheduled:
    scheduled_id = -1
    job_id = data["job_id"]
    scheduled_at = datetime.now(tz=UTC)
    status = models.ScheduledStatus.scheduled

    return schemas.Scheduled(
        scheduled_id=scheduled_id,
        job_id=job_id,
        scheduled_at=scheduled_at,
        status=status,
        )


def convert(scheduled: models.Scheduled) -> dict[str, Any]:
    converted_scheduled = {
            "scheduled_id": scheduled.scheduled_id,
            "job_id": scheduled.job_id,
            "scheduled_at": scheduled.scheduled_at.isoformat(),
            "status": scheduled.status.value,
    }
    return converted_scheduled


def to_dto(scheduled_model: models.Scheduled) -> schemas.Scheduled:
    return schemas.Scheduled(
        scheduled_id=scheduled_model.scheduled_id,
        job_id=scheduled_model.job_id,
        scheduled_at=scheduled_model.scheduled_at,
        status=scheduled_model.status,
        )
