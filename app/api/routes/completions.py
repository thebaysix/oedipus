from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import uuid
import csv
import io
from ...core.database import get_db
from ...services.dataset_service import DatasetService
from ...schemas.completion import CompletionDatasetCreate, CompletionDatasetResponse

router = APIRouter(prefix="/api/v1/datasets", tags=["completions"])


@router.get("/{dataset_id}/completions", response_model=List[CompletionDatasetResponse])
def get_completion_datasets(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get all completion datasets for a given prompt dataset."""
    service = DatasetService(db)
    
    # Verify the dataset exists
    dataset = service.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    completion_datasets = service.get_completion_datasets(dataset_id)
    return [CompletionDatasetResponse.from_orm_with_alias(o) for o in completion_datasets]


@router.post("/{dataset_id}/completions/upload", response_model=CompletionDatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_completion_dataset(
    dataset_id: uuid.UUID,
    file: UploadFile = File(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload an completion dataset from CSV file."""
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
        completions = {}
        reader = csv.DictReader(io.StringIO(csv_content))
        
        # Validate required columns - accept both 'completion_text' and 'output_text' for backward compatibility
        if 'input_id' not in reader.fieldnames:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV must have 'input_id' column"
            )
        
        # Check for completion text column (accept both old and new names)
        completion_col = None
        if 'completion_text' in reader.fieldnames:
            completion_col = 'completion_text'
        elif 'output_text' in reader.fieldnames:
            completion_col = 'output_text'
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV must have either 'completion_text' or 'output_text' column"
            )
        
        for row in reader:
            input_id = row.get('input_id', '').strip()
            completion_text = row.get(completion_col, '').strip()
            
            if not input_id or not completion_text:
                continue  # Skip empty rows
            
            # Handle multiple completions per input_id
            if input_id not in completions:
                completions[input_id] = []
            completions[input_id].append(completion_text)
        
        if not completions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid completion data found in CSV"
            )
        
        # Create completion dataset using existing service
        completion_dataset_create = CompletionDatasetCreate(
            name=name,
            completions=completions,
            metadata={
                "source_file": file.filename,
                "total_completions": sum(len(completion_list) for completion_list in completions.values()),
                "unique_inputs": len(completions)
            }
        )
        
        service = DatasetService(db)
        db_completion = service.create_completion_dataset(dataset_id, completion_dataset_create)
        return CompletionDatasetResponse.from_orm_with_alias(db_completion)
        
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File encoding error. Please ensure the CSV is UTF-8 encoded"
        )
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


@router.post("/{dataset_id}/completions", response_model=CompletionDatasetResponse, status_code=status.HTTP_201_CREATED)
def create_completion_dataset(
    dataset_id: uuid.UUID,
    completion_dataset: CompletionDatasetCreate,
    db: Session = Depends(get_db)
):
    """Create a new completion dataset for a given prompt dataset."""
    try:
        service = DatasetService(db)
        db_completion = service.create_completion_dataset(dataset_id, completion_dataset)
        return CompletionDatasetResponse.from_orm_with_alias(db_completion)
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


@router.get("/{dataset_id}/completions/{completion_id}", response_model=CompletionDatasetResponse)
def get_completion_dataset(
    dataset_id: uuid.UUID,
    completion_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get a specific completion dataset."""
    service = DatasetService(db)
    completion_dataset = service.get_completion_dataset(completion_id)
    
    if not completion_dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Completion dataset not found"
        )
    
    if completion_dataset.dataset_id != dataset_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Completion dataset does not belong to the specified dataset"
        )
    
    return CompletionDatasetResponse.from_orm_with_alias(completion_dataset)