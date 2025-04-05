from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from anthill import models


logger = logging.getLogger(__name__)

class DependenceRepo:
    def add(self, session: Session, completed_job_id: int, trigger_job_id: int,created_at: datetime,
            updated_at: datetime) -> models.Dependence:

        dependence_model = models.Dependence(
                    completed_job_id=completed_job_id,
                    trigger_job_id=trigger_job_id,
                    created_at=created_at,
                    updated_at=updated_at
        )
        try:
            session.add(dependence_model)
            session.commit()
            logger.info("QUERY record successfully inserted.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"QUERY Error: {e}")
        return dependence_model
