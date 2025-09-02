from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import uuid
from ...core.database import get_db
from ...services.comparison_service import ComparisonService
from ...services.export_service import ExportService
from ...schemas.comparison import ComparisonCreate, ComparisonResponse
from ...schemas.export import ExportRequest

router = APIRouter(prefix="/api/v1/comparisons", tags=["comparisons"])


def _run_comparison_analysis_task(comparison_id: str):
    """Background task to run comparison analysis."""
    from ...core.database import SessionLocal
    
    db = SessionLocal()
    try:
        service = ComparisonService(db)
        service.run_comparison_analysis(uuid.UUID(comparison_id))
    except Exception as e:
        print(f"Error running comparison analysis: {e}")
    finally:
        db.close()


def _normalize_comp(c: Any) -> Dict[str, Any]:
    """Convert ORM to response dict with safe defaults to avoid 500s from nulls/legacy rows."""
    return {
        "id": getattr(c, "id"),
        "name": getattr(c, "name"),
        "created_at": getattr(c, "created_at"),
        "datasets": getattr(c, "datasets", None) or [],
        "alignment_key": getattr(c, "alignment_key", None) or "prompt_id",
        "comparison_config": getattr(c, "comparison_config", None) or {},
        "statistical_results": getattr(c, "statistical_results", None) or {},
        "automated_insights": getattr(c, "automated_insights", None) or [],
        "status": getattr(c, "status", None) or "pending",
    }


@router.post("/create", response_model=ComparisonResponse, status_code=status.HTTP_201_CREATED)
def create_comparison(
    payload: ComparisonCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        service = ComparisonService(db)
        comp = service.create_comparison(payload)
        
        # Trigger analysis in background
        background_tasks.add_task(_run_comparison_analysis_task, str(comp.id))
        
        return _normalize_comp(comp)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=List[ComparisonResponse])
def list_comparisons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    service = ComparisonService(db)
    comps = service.list_comparisons(skip=skip, limit=limit)
    return [_normalize_comp(c) for c in comps]


@router.get("/{comparison_id}", response_model=ComparisonResponse)
def get_comparison(
    comparison_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = ComparisonService(db)
    comp = service.get_comparison(comparison_id)
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comparison not found")
    return _normalize_comp(comp)


@router.delete("/{comparison_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comparison(
    comparison_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = ComparisonService(db)
    ok = service.delete_comparison(comparison_id)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comparison not found")
    return None


@router.post("/{comparison_id}/export")
def export_comparison(
    comparison_id: uuid.UUID,
    export_request: ExportRequest,
    db: Session = Depends(get_db)
):
    """Export comparison data in the requested format."""
    try:
        # Validate that the comparison_id in the URL matches the request
        if export_request.comparison_id != comparison_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Comparison ID in URL must match comparison ID in request body"
            )
        
        export_service = ExportService(db)
        content_bytes, filename, content_type = export_service.export_comparison(export_request)
        
        return Response(
            content=content_bytes,
            media_type=content_type,
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Length": str(len(content_bytes))
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))