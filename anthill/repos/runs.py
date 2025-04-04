from sqlalchemy.orm import Session
import logging
from sqlalchemy import select
import datetime as dt
from anthill import models, schemas


logger = logging.getLogger(__name__)


class RunRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def insert(self, prepared_run: schemas.Run) -> None:
        run_model = models.Run(
            run_id=prepared_run.run_id,
            job_id=prepared_run.job_id,
            status=prepared_run.status,
            start_time=prepared_run.start_time,
            created_at=prepared_run.created_at,
            updated_at=prepared_run.updated_at
        )
        try:
            self.session.add(run_model)
            self.session.commit() 
            logger.info("QUERY Record successfully inserted.")
        except Exception as e:
            self.session.rollback()
            logger.error(f"QUERY Error: {e}")
        finally:
            self.session.close()

    def get(self, after: dt) -> list[schemas.Run]:
        query = select(models.Run).where(models.Run.updated_at > after)
        query = query.order_by(models.Run.updated_at)
        result = self.session.execute(query)
        runs = result.scalars().all()
        return [schemas.Run(
            run_id=run.run_id,
            job_id=run.job_id,
            status=run.status,
            start_time=run.start_time,
            created_at=run.created_at,
            updated_at=run.updated_at
        ) for run in runs]
