from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select
from datetime import datetime, timedelta
import logging
from anthill import models
from typing import Sequence
from uuid import UUID


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
            session.refresh(job_model)
            logger.info("QUERY record successfully inserted.")
        except SQLAlchemyError:
            session.rollback()
            logger.exception("unhandled error")
            raise
        return job_model
    
    def get_schedule_jobs_for_run(self, run_id: UUID,
                                  session: Session) -> Sequence[models.Job]:
        CompletedRun = aliased(models.Run)
        DependesRun = aliased(models.Run)
        query = select(models.Job).join(
            models.Dependence,
            models.Dependence.trigger_job_id == models.Job.job_id,
        ).join(
            CompletedRun,
            models.Dependence.completed_job_id == CompletedRun.job_id,
        ).where(CompletedRun.run_id == run_id)

        query = query.join(
            DependesRun,
            DependesRun.job_id == models.Job.job_id,
        ).where(
            DependesRun.updated_at > datetime.now() - timedelta(days=1),
        )

        result = session.execute(query)
        jobs = result.scalars().all()
        return jobs
