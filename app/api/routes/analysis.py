from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
import uuid
from ...core.database import get_db
from ...services.analysis_service import AnalysisService
from ...schemas.analysis import AnalysisJobCreate, AnalysisJobResponse
from ...workers.analysis_worker import run_analysis_task

router = APIRouter(prefix="/api/v1/analysis", tags=["analysis"])


@router.post("/run", response_model=AnalysisJobResponse, status_code=status.HTTP_201_CREATED)
def create_analysis_job(
    job_data: AnalysisJobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Create and start a new analysis job."""
    try:
        service = AnalysisService(db)
        job = service.create_analysis_job(job_data)
        
        # Queue the analysis task
        task = run_analysis_task.delay(str(job.id))
        
        return job
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{job_id}/status", response_model=AnalysisJobResponse)
def get_analysis_job_status(
    job_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get the status of an analysis job."""
    service = AnalysisService(db)
    job = service.get_analysis_job(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis job not found"
        )
    
    return job


@router.get("/{job_id}/results")
def get_analysis_results(
    job_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get the results of a completed analysis job."""
    service = AnalysisService(db)
    job = service.get_analysis_job(job_id)
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis job not found"
        )
    
    if job.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Analysis job is not completed. Current status: {job.status}"
        )
    
    return {
        "job_id": job.id,
        "status": job.status,
        "results": job.results,
        "created_at": job.created_at,
        "completed_at": job.completed_at
    }


@router.post("/run-sync")
def run_analysis_sync(
    job_data: AnalysisJobCreate,
    db: Session = Depends(get_db)
):
    """Run analysis synchronously (for testing/development)."""
    try:
        service = AnalysisService(db)
        job = service.create_analysis_job(job_data)
        
        # Run analysis synchronously
        results = service.run_analysis(job.id)
        
        return {
            "job_id": job.id,
            "status": "completed",
            "results": results
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )