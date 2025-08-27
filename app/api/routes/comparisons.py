from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from ...core.database import get_db
from ...services.comparison_service import ComparisonService
from ...schemas.comparison import ComparisonCreate, ComparisonResponse

router = APIRouter(prefix="/api/v1/comparisons", tags=["comparisons"])


@router.post("/create", response_model=ComparisonResponse, status_code=status.HTTP_201_CREATED)
def create_comparison(
    payload: ComparisonCreate,
    db: Session = Depends(get_db)
):
    try:
        service = ComparisonService(db)
        comp = service.create_comparison(payload)
        return comp  # Pydantic from_attributes handles ORM
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
    return service.list_comparisons(skip=skip, limit=limit)


@router.get("/{comparison_id}", response_model=ComparisonResponse)
def get_comparison(
    comparison_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    service = ComparisonService(db)
    comp = service.get_comparison(comparison_id)
    if not comp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comparison not found")
    return comp


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