from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime, UTC
import logging
from anthill.models import ScheduledStatus, ScheduledTask
from typing import Sequence
from sqlalchemy import select, update

logger = logging.getLogger(__name__)


class ScheduledRepo:
    def add(self, session: Session, job_id: int,
            scheduled_at: datetime,
            status: ScheduledStatus) -> ScheduledTask:
        scheduled_model = ScheduledTask(
            job_id=job_id,
            scheduled_at=scheduled_at,
            status=status
        )
        try:
            session.add(scheduled_model)
            session.commit()
            session.refresh(scheduled_model)
            logger.debug("QUERY Record successfully inserted.")
        except SQLAlchemyError:
            session.rollback()
            logger.exception("unhandled error")
            raise
        return scheduled_model

    def get_scheduled_tasks(
            self, session: Session) -> Sequence[ScheduledTask]:
        query = select(ScheduledTask).where(
            ScheduledTask.status == ScheduledStatus.SCHEDULED)
        result = session.execute(query)
        scheduled_tasks = result.scalars().all()
        return scheduled_tasks

    def update_status_task(self, session: Session,
                           scheduled_task_id: int) -> None:
        query = update(ScheduledTask)
        query = query.where(ScheduledTask.scheduled_id == scheduled_task_id)
        query = query.values(status=ScheduledStatus.TRIGGERED,
                             scheduled_at=datetime.now(tz=UTC))
        session.execute(query)
        session.commit()

    def get_task_by_id(self, task_id: int, session) -> ScheduledTask:
        query = select(ScheduledTask)
        query = query.where(ScheduledTask.scheduled_id == task_id)
        result = session.execute(query)
        task = result.scalars().one_or_none()
        return task
