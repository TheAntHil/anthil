from sqlalchemy.exc import SQLAlchemyError
from anthill.db import get_session
import logging
from sqlalchemy import select
import datetime as dt
from anthill import models, db, schemas, system_handler, job_handler


logger = logging.getLogger(__name__)


def insert_run(prepared_run: schemas.Run) -> None:
    run_model = models.Run(
        run_id=prepared_run.run_id,
        job_id=prepared_run.job_id,
        status=prepared_run.status,
        start_time=prepared_run.start_time,
        created_at=prepared_run.created_at,
        updated_at=prepared_run.updated_at
    )
    session = db.get_session()
    try:
        session.add(run_model)
        session.commit()
        logger.info("QUERY Record successfully inserted.")
    except Exception as e:
        session.rollback()
        logger.error(f"QUERY Error: {e}")
    finally:
        session.close()


def get_runs(after: dt) -> list[schemas.Run]:
    session = db.get_session()
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
        updated_at=run.updated_at
    ) for run in runs]


def insert_system(prepared_system: schemas.System) -> schemas.System:
    system_model = models.System(
        system_id=prepared_system.system_id,
        code=prepared_system.code,
        url=prepared_system.url,
        token=prepared_system.token,
        system_type=prepared_system.system_type
    )
    try:
        with db.get_session() as session:
            session.add(system_model)
            session.commit()
            logger.info("QUERY record successfully inserted.")
            return system_handler.convert_to_dto(system_model)
    except SQLAlchemyError as e:
        logger.error(f"QUERY Error: {e}")


def insert_job(prepared_job: schemas.Job) -> schemas.Job:
    job_model = models.Job(
        job_id=prepared_job.job_id,
        system_id=prepared_job.system_id,
        code=prepared_job.code,
        scheduler=prepared_job.scheduler
    )
    try:
        with get_session() as session:
            session.add(job_model)
            session.commit()
            logger.info("QUERY record successfully inserted.")
            return job_handler.to_dto(job_model)
    except SQLAlchemyError as e:
        logger.error(f"QUERY Error: {e}")
