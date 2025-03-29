from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, UTC
from sqlalchemy import String, ForeignKey
import uuid
from anthill.db import Base


class Run(Base):
    __tablename__ = 'runs'
    run_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))
    start_time: Mapped[datetime] = mapped_column(default=datetime.now(tz=UTC))

    def __repr__(self):
        return (f'<RunModel\n'
                f'run_id={self.run_id}\n'
                f'job_id={self.job_id}\n'
                f'status={self.status}\n'
                f'created_at={self.created_at}\n'
                f'updated_at={self.updated_at}\n'
                f'start_time={self.start_time}>')


class System(Base):
    __tablename__ = 'systems'
    system_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
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

    job_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    system_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("systems.system_id"), nullable=False)
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
