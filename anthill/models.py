from sqlalchemy.dialects.postgresql import UUID
from anthill.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime
import uuid


class RunModel(Base):
    __tablename__ = 'runs'
    run_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column()
    updated_at: Mapped[datetime] = mapped_column()
    start_time: Mapped[datetime] = mapped_column()

    def __repr__(self):
        return (f'<RunModel\n'
                f'{self.run_id}\n'
                f'{self.job_id}\n'
                f'{self.status}\n'
                f'{self.created_at}\n'
                f'{self.updated_at}\n'
                f'{self.start_time}>')


class SystemModel(Base):
    __tablename__ = 'systems'

    system_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    token: Mapped[str] = mapped_column(String(255), nullable=False)
    system_type: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
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