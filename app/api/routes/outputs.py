from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List
import uuid
import csv
import io
from ...core.database import get_db
from ...services.dataset_service import DatasetService
from ...schemas.output import OutputDatasetCreate, OutputDatasetResponse

router = APIRouter(prefix="/api/v1/datasets", tags=["outputs"])


@router.post("/{dataset_id}/outputs/upload", response_model=OutputDatasetResponse, status_code=status.HTTP_201_CREATED)
async def upload_output_dataset(
    dataset_id: uuid.UUID,
    file: UploadFile = File(...),
    name: str = Form(...),
    db: Session = Depends(get_db)
):
    """Upload an output dataset from CSV file."""
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
        outputs = {}
        reader = csv.DictReader(io.StringIO(csv_content))
        
        # Validate required columns
        if 'input_id' not in reader.fieldnames or 'output_text' not in reader.fieldnames:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="CSV must have 'input_id' and 'output_text' columns"
            )
        
        for row in reader:
            input_id = row.get('input_id', '').strip()
            output_text = row.get('output_text', '').strip()
            
            if not input_id or not output_text:
                continue  # Skip empty rows
            
            # Handle multiple outputs per input_id
            if input_id not in outputs:
                outputs[input_id] = []
            outputs[input_id].append(output_text)
        
        if not outputs:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid output data found in CSV"
            )
        
        # Create output dataset using existing service
        output_dataset_create = OutputDatasetCreate(
            name=name,
            outputs=outputs,
            metadata={
                "source_file": file.filename,
                "total_outputs": sum(len(output_list) for output_list in outputs.values()),
                "unique_inputs": len(outputs)
            }
        )
        
        service = DatasetService(db)
        db_output = service.create_output_dataset(dataset_id, output_dataset_create)
        return OutputDatasetResponse.from_orm_with_alias(db_output)
        
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


@router.post("/{dataset_id}/outputs", response_model=OutputDatasetResponse, status_code=status.HTTP_201_CREATED)
def create_output_dataset(
    dataset_id: uuid.UUID,
    output_dataset: OutputDatasetCreate,
    db: Session = Depends(get_db)
):
    """Create a new output dataset for a given input dataset."""
    try:
        service = DatasetService(db)
        db_output = service.create_output_dataset(dataset_id, output_dataset)
        return OutputDatasetResponse.from_orm_with_alias(db_output)
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


@router.get("/{dataset_id}/outputs", response_model=List[OutputDatasetResponse])
def get_output_datasets(
    dataset_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get all output datasets for a given input dataset."""
    service = DatasetService(db)
    
    # Verify the dataset exists
    dataset = service.get_dataset(dataset_id)
    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    output_datasets = service.get_output_datasets(dataset_id)
    return [OutputDatasetResponse.from_orm_with_alias(o) for o in output_datasets]


@router.get("/{dataset_id}/outputs/{output_id}", response_model=OutputDatasetResponse)
def get_output_dataset(
    dataset_id: uuid.UUID,
    output_id: uuid.UUID,
    db: Session = Depends(get_db)
):
    """Get a specific output dataset."""
    service = DatasetService(db)
    output_dataset = service.get_output_dataset(output_id)
    
    if not output_dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Output dataset not found"
        )
    
    if output_dataset.dataset_id != dataset_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Output dataset does not belong to the specified dataset"
        )
    
    return OutputDatasetResponse.from_orm_with_alias(output_dataset)