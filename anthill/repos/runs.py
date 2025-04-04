from sqlalchemy.orm import Session
import logging
from sqlalchemy import select
import datetime as dt
from anthill import models

logger = logging.getLogger(__name__)


class RunRepo:
    def __init__(self) -> None:
        pass

    def insert(self, session: Session, run_id: str, job_id: str, status: str,
               start_time: dt, created_at: dt, updated_at: dt) -> models.Run:
        run_model = models.Run(
            run_id=run_id,
            job_id=job_id,
            status=status,
            start_time=start_time,
            created_at=created_at,
            updated_at=updated_at
        )
        try:
            session.add(run_model)
            session.commit() 
            logger.info("QUERY Record successfully inserted.")
        except Exception as e:
            session.rollback()
            logger.error(f"QUERY Error: {e}")
        return run_model

    def get(self, session: Session, after: dt) -> list[models.Run]:
        query = select(models.Run).where(models.Run.updated_at > after)
        query = query.order_by(models.Run.updated_at)
        result = session.execute(query)
        runs = result.scalars().all()
        return runs
