from sqlalchemy.dialects.postgresql import UUID
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
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
