from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
import logging
from sqlalchemy import select
from datetime import datetime, UTC
from anthill import models
from typing import Sequence

logger = logging.getLogger(__name__)


class RunRepo:
    def add(self, session: Session, run_id: str, job_id: int,
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
            logger.info("QUERY Record successfully inserted.")
        except SQLAlchemyError:
            session.rollback()
            logger.exception("unhandled error")
            raise
        return run_model

    def get_updates(self, session: Session,
                    after: datetime) -> Sequence[models.Run]:
        query = select(models.Run).where(models.Run.updated_at > after)
        query = query.order_by(models.Run.updated_at)
        result = session.execute(query)
        runs = result.scalars().all()
        for run in runs:
            run.status = models.RunStatus.SCHEDULED
            run.updated_at = datetime.now(tz=UTC)
        session.commit()
        return runs
