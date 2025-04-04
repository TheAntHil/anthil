from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from anthill import models


logger = logging.getLogger(__name__)


class SystemRepo:
    def add(self, session: Session, system_id: str, code: str, url: str,
            token: str, system_type: str, created_at: datetime,
            updated_at: datetime) -> models.System:
        system_model = models.System(
                    system_id=system_id,
                    code=code,
                    url=url,
                    token=token,
                    system_type=system_type,
                    created_at=created_at,
                    updated_at=updated_at
        )
        try:
            session.add(system_model)
            session.commit()
            logger.info("QUERY record successfully inserted.")
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"QUERY Error: {e}")
        return system_model
