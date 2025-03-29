from datetime import datetime
from typing import Optional
import dataclasses as dc


@dc.dataclass
class Run:
    run_id: str
    job_id: str
    status: str
    start_time: datetime
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dc.dataclass
class System:
    system_id: str
    code: str
    url: str
    token: str
    system_type: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dc.dataclass
class Job:
    job_id: str
    system_id: str
    code: str
    scheduler: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
