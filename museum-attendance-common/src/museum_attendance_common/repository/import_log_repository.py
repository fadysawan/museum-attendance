from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from museum_attendance_common.model import ImportLog
from museum_attendance_common.enumeration import ImportStatus
from datetime import datetime, timezone
from museum_attendance_common.utils import get_logger
from museum_attendance_common.exceptions import DatabaseError

logger = get_logger(__name__)

class ImportLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def start_job(self, status: ImportStatus, result: dict[str, int | str] | None = None) -> ImportLog:
        try:
            import_log = ImportLog(
                status=status.value,
                result=result
            )
            self.session.add(import_log)
            self.session.flush()
            logger.info(f"Started import job with status: {status.value}")
            return import_log
        except SQLAlchemyError as e:
            logger.error(f"Error starting import job: {str(e)}")
            raise DatabaseError(f"Failed to start import job: {str(e)}", entity_type="ImportLog", operation="start_job") from e
    
    def end_job_with_failure(self, import_log: ImportLog, result: dict[str, int | str] | None = None) -> ImportLog:
        try:
            import_log.status = ImportStatus.FAILED.value
            import_log.result = result
            import_log.completed_at = datetime.now(timezone.utc)
            self.session.flush()
            logger.info(f"Import job {import_log.id} ended with failure")
            return import_log
        except SQLAlchemyError as e:
            logger.error(f"Error ending import job with failure: {str(e)}")
            raise DatabaseError(f"Failed to end import job: {str(e)}", entity_type="ImportLog", operation="end_job_with_failure") from e
    
    def end_job_with_success(self, import_log: ImportLog, result: dict[str, int | str] | None = None) -> ImportLog:
        try:
            import_log.status = ImportStatus.SUCCESS.value
            import_log.result = result
            import_log.completed_at = datetime.now(timezone.utc)
            self.session.flush()
            logger.info(f"Import job {import_log.id} ended with success")
            return import_log
        except SQLAlchemyError as e:
            logger.error(f"Error ending import job with success: {str(e)}")
            raise DatabaseError(f"Failed to end import job: {str(e)}", entity_type="ImportLog", operation="end_job_with_success") from e