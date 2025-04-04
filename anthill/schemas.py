from datetime import datetime
import dataclasses as dc


@dc.dataclass
class Run:
    run_id: str
    job_id: str
    status: str
    start_time: datetime
    created_at: datetime | None
    updated_at: datetime | None


@dc.dataclass
class SystemDTO:
    system_id: str
    code: str
    url: str
    token: str
    system_type: str
    created_at: datetime | None
    updated_at: datetime | None


@dc.dataclass
class JobDTO:
    job_id: str
    system_id: str
    code: str
    scheduler: str
    created_at: datetime | None
    updated_at: datetime | None

@dc.dataclass
class DependenceDTO:
    dependence_id: str
    child_code: str
    parent_code: str
    parent_scheduler: str
    created_at: datetime | None
    updated_at: datetime | None