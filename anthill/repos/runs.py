from sqlalchemy.orm import Session
import logging
from sqlalchemy import select
import datetime as dt
from anthill import models, schemas

logger = logging.getLogger(__name__)


class RunRepo:
    def __init__(self) -> None:
        pass

    def insert(self, session: Session, run_id: str, job_id: str, status: str,
               start_time: dt, created_at: dt, updated_at: dt) -> None:
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

    def get(self, session: Session, after: dt) -> list[schemas.Run]:
        query = select(models.Run).where(models.Run.updated_at > after)
        query = query.order_by(models.Run.updated_at)
        result = session.execute(query)
        runs = result.scalars().all()
        return [schemas.Run(
                run_id=run.run_id,
                job_id=run.job_id,
                status=run.status,
                start_time=run.start_time,
                created_at=run.created_at,
                updated_at=run.updated_at) for run in runs]
