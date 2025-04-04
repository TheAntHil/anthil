from sqlalchemy.exc import SQLAlchemyError
from anthill.db import get_session
import logging
from anthill import models, db, schemas, system_handler, job_handler


logger = logging.getLogger(__name__)


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
