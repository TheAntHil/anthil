from anthill.models import RunModel
from anthill.db import get_session
from anthill.signal_handler import Run
import logging


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
        logger.info(f"QUERY  Record successfully inserted.")
    except Exception as e:
        session.rollback()
        logger.error(f"QUERY Error: {e}")
    finally:
        session.close()
