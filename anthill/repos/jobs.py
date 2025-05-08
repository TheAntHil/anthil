from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, distinct
from sqlalchemy.sql.functions import coalesce, count
from datetime import datetime, timedelta, UTC
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
            logger.debug(
                "QUERY: JobRepo.add — inserted job "
                f"(system_id={system_id}, "
                f"(code='{code}', "
                f"(scheduler='{scheduler}')")
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(
                f"QUERY FAILED: JobRepo.add — "
                f"(system_id={system_id}, "
                f"(code='{code}', "
                f"(scheduler='{scheduler}')"
                f" - {e}")
            raise
        return job_model

    def get_schedule_jobs_for_run(self, run_id: UUID,
                                  session: Session) -> Sequence[tuple[int, int]]:
        CompletedRun = aliased(models.Run)
        DependesRun = aliased(models.Run)
        OtherRun = aliased(models.Run)

        DependenceOne = aliased(models.Dependence)
        DependenceTwo = aliased(models.Dependence)
        
        actuality_time = datetime.now(tz=UTC) - timedelta(minutes=1)
        query = select(models.Job.job_id, count(distinct(OtherRun.job_id))).join(
            DependenceOne,
            DependenceOne.trigger_job_id == models.Job.job_id,
        ).join(
            CompletedRun,
            DependenceOne.completed_job_id == CompletedRun.job_id,
        ).where(CompletedRun.run_id == run_id)
        
        query = query.join(
            DependenceTwo,
            DependenceTwo.trigger_job_id == models.Job.job_id   
        )
        query = query.join(
            OtherRun,
            DependenceTwo.completed_job_id == OtherRun.job_id,
        ).where(OtherRun.updated_at > actuality_time)

        query = query.join(
            DependesRun,
            DependesRun.job_id == models.Job.job_id, isouter=True,
        ).where(
            coalesce(
                DependesRun.updated_at,
                datetime(1970, 1, 1)) < actuality_time,
        )

        query = query.group_by(models.Job.job_id)

        logger.debug(
            f"QUERY: JobRepo.get_schedule_jobs_for_run — run_id={run_id}")
        result = session.execute(query)
        jobs = result.all()
        return jobs

    def get_jobs_by_id(self, job_id: int,
                       session: Session) -> models.Job | None:
        query = select(models.Job).where(models.Job.job_id == job_id)
        logger.debug(f"QUERY: JobRepo.get_jobs_by_id — job_id={job_id}")
        result = session.execute(query)
        job = result.scalars().one_or_none()
        return job
