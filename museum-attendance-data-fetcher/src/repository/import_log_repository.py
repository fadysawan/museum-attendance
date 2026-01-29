from sqlalchemy.orm import Session
from model import ImportLog
from enumeration import ImportStatus
from datetime import datetime, timezone

class ImportLogRepository:
    def __init__(self, session: Session):
        self.session = session

    def start_job(self, status: ImportStatus, result: dict = None) -> ImportLog:
        import_log = ImportLog(
            status=status.value,
            result=result
        )
        self.session.add(import_log)
        self.session.flush()
        return import_log
    
    def end_job_with_failure(self, import_log: ImportLog, result: dict = None) -> ImportLog:
        import_log.status = ImportStatus.FAILED.value
        import_log.result = result
        import_log.completed_at = datetime.now(timezone.utc)
        self.session.flush()
        return import_log
    
    def end_job_with_success(self, import_log: ImportLog, result: dict = None) -> ImportLog:
        import_log.status = ImportStatus.SUCCESS.value
        import_log.result = result
        import_log.completed_at = datetime.now(timezone.utc)
        self.session.flush()
        return import_log