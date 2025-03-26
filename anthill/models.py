from sqlalchemy.dialects.postgresql import UUID
from anhill.db import Base, engine
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid


class Run(Base):
    __tablename__ = 'runs'
    run_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    job_id: Mapped[uuid.UUID]
    status: Mapped[str]
    created_at: Mapped[datetime]
    updated_at: Mapped[datetime]
    start_time: Mapped[datetime]

    def __repr__(self):
        return f'<Run {self.run_id} {self.job_id} {self.status}>'

# if __name__ == "__main__":
#     Base.metadata.create_all(bind=engine)
