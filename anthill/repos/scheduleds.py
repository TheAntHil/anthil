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
            logger.debug(
                f"QUERY: ScheduledRepo.add — inserted scheduled task "
                f"(job_id={job_id}, "
                f"scheduled_at={scheduled_at}, "
                f"status={status})")
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(
                f"QUERY FAILED: ScheduledRepo.add — "
                f"(job_id={job_id}, "
                f"scheduled_at={scheduled_at}, "
                f"status={status}) "
                f"— {e}")
            raise
        return scheduled_model

    def get_scheduled_tasks(
            self, session: Session) -> Sequence[ScheduledTask]:
        try:
            query = select(ScheduledTask).where(
                ScheduledTask.status == ScheduledStatus.SCHEDULED)
            logger.debug("QUERY: ScheduledRepo.get_scheduled_tasks")
            result = session.execute(query)
            scheduled_tasks = result.scalars().all()
        except SQLAlchemyError as e:
            logger.exception(f"QUERY FAILED: ScheduledRepo.get_scheduled_tasks"
                             f"— {e}")
            raise
        return scheduled_tasks

    def update_status_task(self, session: Session,
                           scheduled_task_id: int) -> None:
        try:
            query = update(ScheduledTask)
            query = query.where(ScheduledTask.scheduled_id ==
                                scheduled_task_id)
            query = query.values(status=ScheduledStatus.TRIGGERED,
                                 scheduled_at=datetime.now(tz=UTC))
            session.execute(query)
            session.commit()
            logger.debug(f"QUERY: Upd status task_id={scheduled_task_id}")
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(f"QUERY FAILED: ScheduledRepo.update_status_task "
                             f"— task_id={scheduled_task_id} — {e}")
            raise

    def get_task_by_id(self, task_id: int, session) -> ScheduledTask:
        try:
            query = select(ScheduledTask)
            query = query.where(ScheduledTask.scheduled_id == task_id)
            logger.debug(f"QUERY: ScheduledRepo.get_task_by_id "
                         f"— task_id={task_id}")
            result = session.execute(query)
            task = result.scalars().one_or_none()
        except SQLAlchemyError as e:
            logger.exception(f"QUERY FAILED: ScheduledRepo.get_task_by_id "
                             f"— task_id={task_id} — {e}")
            raise
        return task
