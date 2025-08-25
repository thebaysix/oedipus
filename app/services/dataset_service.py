from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from ..models.dataset import Dataset
from ..models.output import OutputDataset
from ..schemas.dataset import DatasetCreate
from ..schemas.output import OutputDatasetCreate


class DatasetService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_dataset(self, dataset_data: DatasetCreate, user_id: uuid.UUID) -> Dataset:
        """Create a new dataset."""
        db_dataset = Dataset(
            name=dataset_data.name,
            user_id=user_id,
            inputs=dataset_data.inputs,
            user_metadata=dataset_data.metadata
        )
        self.db.add(db_dataset)
        self.db.commit()
        self.db.refresh(db_dataset)
        return db_dataset
    
    def get_dataset(self, dataset_id: uuid.UUID) -> Optional[Dataset]:
        """Get a dataset by ID."""
        return self.db.query(Dataset).filter(Dataset.id == dataset_id).first()
    
    def get_datasets(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Dataset]:
        """Get all datasets for a user."""
        return (
            self.db.query(Dataset)
            .filter(Dataset.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def create_output_dataset(self, dataset_id: uuid.UUID, output_data: OutputDatasetCreate) -> OutputDataset:
        """Create a new output dataset."""
        # Verify the parent dataset exists
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        # Validate that output keys match input keys
        input_keys = set(dataset.inputs.keys())
        output_keys = set(output_data.outputs.keys())
        
        if not output_keys.issubset(input_keys):
            missing_keys = output_keys - input_keys
            raise ValueError(f"Output keys not found in input dataset: {missing_keys}")
        
        db_output = OutputDataset(
            name=output_data.name,
            dataset_id=dataset_id,
            outputs=output_data.outputs,
            user_metadata=output_data.metadata
        )
        self.db.add(db_output)
        self.db.commit()
        self.db.refresh(db_output)
        return db_output
    
    def get_output_dataset(self, output_id: uuid.UUID) -> Optional[OutputDataset]:
        """Get an output dataset by ID."""
        return self.db.query(OutputDataset).filter(OutputDataset.id == output_id).first()
    
    def get_output_datasets(self, dataset_id: uuid.UUID) -> List[OutputDataset]:
        """Get all output datasets for a dataset."""
        return (
            self.db.query(OutputDataset)
            .filter(OutputDataset.dataset_id == dataset_id)
            .all()
        )