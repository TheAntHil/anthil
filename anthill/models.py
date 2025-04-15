from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC
from sqlalchemy import String, ForeignKey, Enum, UniqueConstraint
from uuid import UUID
from anthill.db import Base
from enum import Enum as PyEnum


class RunStatus(PyEnum):
    created = "created"
    scheduled = "scheduled"
    triggered = "triggered"


class Run(Base):
    __tablename__ = 'runs'

    run_id: Mapped[UUID] = mapped_column(primary_key=True)
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id"))
    external_status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    start_time: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    status: Mapped[RunStatus] = mapped_column(
        Enum(RunStatus, name="run_status"),
        nullable=False,
        default=RunStatus.created)

    def __repr__(self):
        return (f'<RunModel\n'
                f'run_id={self.run_id}\n'
                f'job_id={self.job_id}\n'
                f'external_status={self.external_status}\n'
                f'created_at={self.created_at}\n'
                f'updated_at={self.updated_at}\n'
                f'start_time={self.start_time}\n'
                f'status={self.status}>')


class System(Base):
    __tablename__ = 'systems'

    system_id: Mapped[int] = mapped_column(primary_key=True,
                                           autoincrement=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    system_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        onupdate=datetime.now(tz=UTC)
    )

    def __repr__(self):
        return (f'<System\n'
                f'system_id={self.system_id}\n'
                f'code={self.code}\n'
                f'url={self.url}\n'
                f'token={self.token}\n'
                f'system_type={self.system_type}\n'
                f'created_at={self.created_at}\n'
                f'updated_at={self.updated_at}>')


class Job(Base):
    __tablename__ = 'jobs'

    job_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    system_id: Mapped[int] = mapped_column(ForeignKey("systems.system_id"),
                                           nullable=False)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    scheduler: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        onupdate=datetime.now(tz=UTC)
    )

    def __repr__(self):
        return (f'<Job\n'
                f'job_id={self.job_id}\n'
                f'system_id={self.system_id}\n'
                f'code={self.code}\n'
                f'url={self.url}\n'
                f'scheduler={self.scheduler}\n'
                f'created_at={self.created_at}\n'
                f'updated_at={self.updated_at}>')


class Dependence(Base):
    __tablename__ = 'job_dependencies'

    dependence_id: Mapped[int] = mapped_column(primary_key=True,
                                               autoincrement=True)
    completed_job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id"))
    trigger_job_id: Mapped[int] = mapped_column(ForeignKey("jobs.job_id"))
    # parent_scheduler: Mapped[str] = mapped_column(String(255),
    #                                               nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(tz=UTC),
        onupdate=datetime.now(tz=UTC)
    )
    __table_args__ = (
        UniqueConstraint('completed_job_id', 'trigger_job_id',
                         name='unique_index_job_dependence'),
    )

    def __repr__(self):
        return (f'<Dependence\n'
                f'dependence_id={self.dependence_id}\n'
                f'child_code={self.completed_job_id}\n'
                f'parent_code={self.trigger_job_id}\n'
                # f'parent_scheduler={self.parent_scheduler}\n'
                f'created_at={self.created_at}\n'
                f'updated_at={self.updated_at}>')
