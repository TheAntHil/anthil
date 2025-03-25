import uuid
from datetime import datetime, UTC
from typing import Any
import dataclasses as dc


@dc.dataclass
class Run:
    run_id: str
    job_id: str
    status: str
    start_time: datetime
    created_at: datetime
    updated_at: datetime


def process_signal(data: dict[str, Any]) -> Run:
    status = data["status"]
    start_time = data["start_time"]
    run_id = str(uuid.uuid4())
    job_id = str(uuid.uuid4())
    created_at = datetime.now(tz=UTC).isoformat()
    updated_at = datetime.now(tz=UTC).isoformat()

    return Run(
        run_id=run_id,
        job_id=job_id,
        status=status,
        start_time=start_time,
        created_at=created_at,
        updated_at=updated_at)
