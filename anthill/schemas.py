from datetime import datetime
import dataclasses as dc


@dc.dataclass
class Run:
    run_id: str
    job_id: int
    externol_status: str
    start_time: datetime
    created_at: datetime
    updated_at: datetime


@dc.dataclass
class System:
    system_id: int
    code: str
    url: str
    token: str
    system_type: str
    created_at: datetime
    updated_at: datetime


@dc.dataclass
class Job:
    job_id: int
    system_id: int
    code: str
    scheduler: str
    created_at: datetime
    updated_at: datetime


@dc.dataclass
class Dependence:
    dependence_id: int
    completed_job_id: int
    trigger_job_id: int
    # parent_scheduler: str
    created_at: datetime
    updated_at: datetime
