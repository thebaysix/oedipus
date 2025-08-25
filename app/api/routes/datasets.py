from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from ...core.database import get_db
from ...services.dataset_service import DatasetService
from ...schemas.dataset import DatasetCreate, DatasetResponse

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])

# Mock user ID for MVP (in production, this would come from authentication)
MOCK_USER_ID = uuid.uuid4()


@router.post("/", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
def create_dataset(
    dataset: DatasetCreate,
    db: Session = Depends(get_db)
):
    """Create a new dataset."""
    try:
        service = DatasetService(db)
        db_dataset = service.create_dataset(dataset, MOCK_USER_ID)
        return DatasetResponse.from_orm_with_alias(db_dataset)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[DatasetResponse])
def get_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all datasets for the current user."""
    service = DatasetService(db)
    datasets = service.get_datasets(MOCK_USER_ID, skip=skip, limit=limit)
    return [DatasetResponse.from_orm_with_alias(d) for d in datasets]


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get a specific dataset by ID."""
    service = DatasetService(db)
    dataset = service.get_dataset(dataset_id)
    
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    return DatasetResponse.from_orm_with_alias(dataset)