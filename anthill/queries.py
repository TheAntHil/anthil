from anthill.models import RunModel
from anthill.db import get_session
from anthill.signal_handler import Run
import logging
from sqlalchemy import select
from datetime import datetime as dt


logger = logging.getLogger(__name__)


def insert_run(prepared_run: Run) -> None:
    run_model = RunModel(
        run_id=prepared_run.run_id,
        job_id=prepared_run.job_id,
        status=prepared_run.status,
        start_time=prepared_run.start_time,
        created_at=prepared_run.created_at,
        updated_at=prepared_run.updated_at
    )
    session = get_session()
    try:
        session.add(run_model)
        session.commit()
        logger.info("QUERY  Record successfully inserted.")
    except Exception as e:
        session.rollback()
        logger.error(f"QUERY Error: {e}")
    finally:
        session.close()


def get_runs_by_db(after, sort) -> None:
    session = get_session()
    query = select(RunModel).where(RunModel.updated_at > after)
    sort_field = getattr(RunModel, sort)
    query = query.order_by(sort_field)
    result = session.execute(query)
    runs = result.scalars().all()
    return [Run(
        run_id=run.run_id,
        job_id=run.job_id,
        status=run.status,
        start_time=run.start_time,
        created_at=run.created_at,
        updated_at=run.updated_at
    ) for run in runs]
