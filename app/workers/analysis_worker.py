from celery import Celery
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from ..core.config import settings
from ..services.analysis_service import AnalysisService
from ..models import *  # Ensure all models are registered with SQLAlchemy before use

# Database setup for worker
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Celery app (only enable Redis/Celery if not local)
if settings.OEDIPUS_ENV == "local" or not settings.REDIS_URL:
    celery_app = None
else:
    celery_app = Celery(
        "oedipus_worker",
        broker=settings.celery_broker_url,
        backend=settings.celery_result_backend,
    )

    # Configure Celery
    celery_app.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        task_soft_time_limit=25 * 60,  # 25 minutes
        worker_prefetch_multiplier=1,
        worker_max_tasks_per_child=1000,
    )


if celery_app:
    @celery_app.task(bind=True)
    def run_analysis_task(self, job_id: str):
        """
        Celery task to run analysis job.
        """
        db = SessionLocal()
        try:
            analysis_service = AnalysisService(db)
            job_uuid = uuid.UUID(job_id)

            # Update task progress
            self.update_state(
                state="PROGRESS",
                meta={"current": 0, "total": 100, "status": "Starting analysis..."}
            )

            # Run the analysis
            results = analysis_service.run_analysis(job_uuid)

            # Update task progress
            self.update_state(
                state="PROGRESS",
                meta={"current": 100, "total": 100, "status": "Analysis completed"}
            )

            return {
                "status": "completed",
                "results": results
            }

        except Exception as exc:
            # Update task state to failure
            self.update_state(
                state="FAILURE",
                meta={"error": str(exc)}
            )
            raise
        finally:
            db.close()


    @celery_app.task
    def health_check():
        """Simple health check task."""
        return {"status": "healthy", "message": "Worker is running"}

else:
    # Local synchronous fallback
    def run_analysis_task(job_id: str):
        """
        Synchronous fallback for local development.
        """
        db = SessionLocal()
        try:
            analysis_service = AnalysisService(db)
            job_uuid = uuid.UUID(job_id)
            return analysis_service.run_analysis(job_uuid)
        finally:
            db.close()

    def health_check():
        """Synchronous health check for local development."""
        return {"status": "healthy", "message": "Worker is running"}


if __name__ == "__main__":
    if celery_app:
        celery_app.start()
    else:
        print("Celery app not enabled (local mode). Tasks can be run synchronously.")
