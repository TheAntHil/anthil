from datetime import datetime
import dataclasses as dc
from typing import Optional


@dc.dataclass
class Run:
    run_id: str
    job_id: int | None
    status: str
    start_time: datetime
    created_at: datetime | None
    updated_at: datetime | None


@dc.dataclass
class System:
    system_id: int
    code: str
    url: str
    token: str
    system_type: str
    created_at: datetime | None
    updated_at: datetime | None


@dc.dataclass
class Job:
    job_id: int
    system_id: int
    code: str
    scheduler: str
    created_at: datetime | None
    updated_at: datetime | None



@dc.dataclass
class Dependence:
    dependence_id: int
    completed_job_id: int
    trigger_job_id: int
    # parent_scheduler: str
    created_at: datetime | None
    updated_at: datetime | None