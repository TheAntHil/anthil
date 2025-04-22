from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from anthill import models
from typing import Sequence
from sqlalchemy import select

logger = logging.getLogger(__name__)


class ScheduledRepo:
    def add(self, session: Session, job_id: int,
            scheduled_at: datetime,
            status: models.ScheduledStatus) -> models.ScheduledTask:
        scheduled_model = models.ScheduledTask(
            job_id=job_id,
            scheduled_at=scheduled_at,
            status=status
        )
        try:
            session.add(scheduled_model)
            session.commit()
            session.refresh(scheduled_model)
            logger.info("QUERY Record successfully inserted.")
        except SQLAlchemyError:
            session.rollback()
            logger.exception("unhandled error")
            raise
        return scheduled_model

    def get_scheduled_tasks(
            self, session: Session) -> Sequence[models.ScheduledTask]:
        query = select(models.ScheduledTask).where(
            models.ScheduledTask.status == models.ScheduledStatus.SCHEDULED)
        result = session.execute(query)
        scheduled_tasks = result.scalars().all()
        return scheduled_tasks
