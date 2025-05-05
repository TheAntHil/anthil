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
            logger.debug(
                f"QUERY: SystemRepo.add — inserted system "
                f"(code={code}, url={url}, "
                f"system_type={system_type}, "
                f"created_at={created_at}, "
                f"updated_at={updated_at})")
        except SQLAlchemyError as e:
            session.rollback()
            logger.exception(
                f"QUERY FAILED: SystemRepo.add — "
                f"(code={code}, "
                f"url={url}, "
                f"system_type={system_type}, "
                f"created_at={created_at}, "
                f"updated_at={updated_at}) "
                f"— {e}")
            raise
        return system_model

    def get_system_by_id(self, system_id: int,
                         session: Session) -> models.System | None:
        try:
            query = select(models.System)
            query = query.where(models.System.system_id == system_id)
            logger.debug(f"QUERY: SystemRepo.get_system_by_id "
                         f"— system_id={system_id}")
            result = session.execute(query)
            system = result.scalars().one_or_none()
        except SQLAlchemyError as e:
            logger.exception(f"QUERY FAILED: SystemRepo.get_system_by_id "
                             f"— system_id={system_id} — {e}")
            raise
        return system
