import uuid
from datetime import datetime, UTC
from typing import Any
from anthill import schemas


def process_run(data: dict[str, Any]) -> schemas.Run:
    status = data["status"]
    start_time = datetime.fromisoformat(data["start_time"])
    run_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    created_at = datetime.now(tz=UTC)
    updated_at = datetime.now(tz=UTC)

    return schemas.Run(
        run_id=run_id,
        job_id=job_id,
        status=status,
        start_time=start_time,
        created_at=created_at,
        updated_at=updated_at)


def convert(run: schemas.Run) -> dict[str, Any]:
    converted_run = {
        "run_id": run.run_id,
        "job_id": run.job_id,
        "status": run.status,
        "start_time": run.start_time.isoformat(),
        "created_at": run.created_at.isoformat(),
        "updated_at": run.updated_at.isoformat()
    }
    return converted_run
