from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import uuid
import csv
import io
from ...core.database import get_db
from ...services.dataset_service import DatasetService
from ...schemas.dataset import DatasetCreate, DatasetResponse

router = APIRouter(prefix="/api/v1/datasets", tags=["datasets"])

# Mock user ID for MVP (in production, this would come from authentication)
MOCK_USER_ID = uuid.uuid4()


@router.post("/upload", response_model=DatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload a dataset from CSV file."""
    try:
        # Validate file type
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be a CSV file"
            )
        
        # Read and parse CSV
        content = await file.read()
        csv_content = content.decode('utf-8')
        
        # Parse CSV data
        prompts = {}
        reader = csv.DictReader(io.StringIO(csv_content))
        
        # Validate required columns
        if 'prompt_id' not in reader.fieldnames or 'prompt_text' not in reader.fieldnames:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV must have 'prompt_id' and 'prompt_text' columns"
            )
        
        for row in reader:
            prompt_id = row.get('prompt_id', '').strip()
            prompt_text = row.get('prompt_text', '').strip()
            
            if not prompt_id or not prompt_text:
                continue  # Skip empty rows
                
            prompts[prompt_id] = prompt_text
        
        if not prompts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid prompt data found in CSV"
            )
        
        # Create dataset using existing service
        dataset_create = DatasetCreate(
            name=name,
            prompts=prompts,
            metadata={
                "source_file": file.filename,
                "total_inputs": len(prompts)
            }
        )
        
        service = DatasetService(db)
        db_dataset = service.create_dataset(dataset_create, MOCK_USER_ID)
        return DatasetResponse.from_orm_with_alias(db_dataset)
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File encoding error. Please ensure the CSV is UTF-8 encoded"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


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