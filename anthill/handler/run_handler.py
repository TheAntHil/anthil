import uuid
from datetime import datetime, UTC
from typing import Any
from anthill import schemas, models


def process_run(data: dict[str, Any]) -> schemas.Run:
    external_status = data["external_status"]
    start_time = datetime.fromisoformat(data["start_time"])
    run_id = str(uuid.uuid4())
    job_id = data["job_id"]
    created_at = datetime.now(tz=UTC)
    updated_at = datetime.now(tz=UTC)
    status = models.RunStatus.created

    return schemas.Run(
        run_id=run_id,
        job_id=job_id,
        external_status=external_status,
        start_time=start_time,
        created_at=created_at,
        updated_at=updated_at,
        status=status,
        )


def convert(run: models.Run) -> dict[str, Any]:
    converted_run = {
        "run_id": run.run_id,
        "job_id": run.job_id,
        "external_status": run.external_status,
        "start_time": run.start_time.isoformat(),
        "created_at": run.created_at.isoformat(),
        "updated_at": run.updated_at.isoformat(),
        "status": run.status.value,
    }
    return converted_run
