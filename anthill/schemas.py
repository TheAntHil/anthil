from datetime import datetime
from anthill.models import RunStatus, ScheduledStatus
from pydantic import BaseModel, ConfigDict
from uuid import UUID


class Run(BaseModel):
    run_id: UUID
    job_id: int
    external_status: str
    start_time: datetime
    created_at: datetime
    updated_at: datetime
    status: RunStatus

    model_config = ConfigDict(from_attributes=True)


class RunCreate(BaseModel):
    job_id: int
    external_status: str
    start_time: datetime

    model_config = ConfigDict(from_attributes=True)


class System(BaseModel):
    system_id: int
    code: str
    url: str
    token: str
    system_type: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Job(BaseModel):
    job_id: int
    system_id: int
    code: str
    scheduler: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Dependence(BaseModel):
    dependence_id: int
    completed_job_id: int
    trigger_job_id: int
    # parent_scheduler: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Scheduled(BaseModel):
    scheduled_id: int
    job_id: int
    scheduled_at: datetime
    status: ScheduledStatus

    model_config = ConfigDict(from_attributes=True)
