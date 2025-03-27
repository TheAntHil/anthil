from sqlalchemy.dialects.postgresql import UUID
from .db import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid


class Run(Base):
    __tablename__ = 'runs'
    run_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    job_id: Mapped[int]
    status: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    start_time: Mapped[datetime]

    def __repr__(self):
        return (f'<Run\n'
                f'{self.run_id}\n'
                f'{self.job_id}\n'
                f'{self.status}\n'
                f'{self.created_at}\n'
                f'{self.updated_at}\n'
                f'{self.start_time}>')
