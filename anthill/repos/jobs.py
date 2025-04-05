from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from anthill import models


logger = logging.getLogger(__name__)


class JobRepo:
    def add(self, session: Session, system_id: int, code: str,
            scheduler: str, created_at: datetime,
            updated_at: datetime) -> models.Job:
        job_model = models.Job(
                    system_id=system_id,
                    code=code,
                    scheduler=scheduler,
                    created_at=created_at,
                    updated_at=updated_at
        )
        try:
            session.add(job_model)
            session.commit()
            logger.info("QUERY record successfully inserted.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"QUERY Error: {e}")
        return job_model
