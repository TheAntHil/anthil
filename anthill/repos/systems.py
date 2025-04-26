from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
import logging
from anthill import models


logger = logging.getLogger(__name__)


class SystemRepo:
    def add(self, session: Session, code: str, url: str,
            token: str, system_type: str, created_at: datetime,
            updated_at: datetime) -> models.System:
        system_model = models.System(
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
            session.refresh(system_model)
            logger.info("QUERY record successfully inserted.")
        except SQLAlchemyError:
            session.rollback()
            logger.exception("unhandled error")
            raise
        return system_model

    def get_system_by_id(self, system_id: int,
                         session: Session) -> models.System | None:
        query = select(models.System)
        query = query.where(models.System.system_id == system_id)
        result = session.execute(query)
        system = result.scalars().one_or_none()
        return system
