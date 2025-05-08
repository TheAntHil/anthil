from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging
from sqlalchemy import select
from datetime import datetime, UTC
from anthill import models
from typing import Sequence
from uuid import UUID

logger = logging.getLogger(__name__)


class RunRepo:
    def add(self, session: Session, run_id: UUID, job_id: int,
            external_status: str, start_time: datetime, created_at: datetime,
            updated_at: datetime, status: models.RunStatus) -> models.Run:
        run_model = models.Run(
            run_id=run_id,
            job_id=job_id,
            external_status=external_status,
            start_time=start_time,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
        )
        try:
            session.add(run_model)
            session.commit()
            session.refresh(run_model)
            logger.debug(
                f"QUERY: RunRepo.add — inserted run "
                f"(run_id={run_id}, "
                f"(job_id={job_id}, "
                f"status={status})")
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(
                f"QUERY FAILED: RunRepo.add — "
                f"(run_id={run_id}, "
                f"job_id={job_id}, "
                f"status={status}) "
                f"— {e}")
            raise
        return run_model

    def acquire(self, session: Session) -> Sequence[models.Run]:
        try:
            query = select(models.Run)
            query = query.where(models.Run.status == models.RunStatus.CREATED)
            query = query.order_by(models.Run.updated_at)
            logger.debug("start: acquire created runs")
            result = session.execute(query)
            runs = result.scalars().all()
            for run in runs:
                run.status = models.RunStatus.SCHEDULED
                run.updated_at = datetime.now(tz=UTC)
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception("failed: acquire created runs %s", e)
        return runs
