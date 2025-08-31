from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from ..models.dataset import Dataset
from ..models.completion import CompletionDataset
from ..schemas.dataset import DatasetCreate
from ..schemas.completion import CompletionDatasetCreate


class DatasetService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_dataset(self, dataset_data: DatasetCreate, user_id: uuid.UUID) -> Dataset:
        """Create a new dataset."""
        db_dataset = Dataset(
            name=dataset_data.name,
            user_id=user_id,
            prompts=dataset_data.prompts,
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
    
    def create_completion_dataset(self, dataset_id: uuid.UUID, output_data: CompletionDatasetCreate) -> CompletionDataset:
        """Create a new completion dataset."""
        # Verify the parent dataset exists
        dataset = self.get_dataset(dataset_id)
        if not dataset:
            raise ValueError(f"Dataset {dataset_id} not found")
        
        # Validate that output keys match prompt keys
        input_keys = set(dataset.prompts.keys())
        output_keys = set(output_data.completions.keys())
        
        if not output_keys.issubset(input_keys):
            missing_keys = output_keys - input_keys
            raise ValueError(f"Output keys not found in prompt dataset: {missing_keys}")
        
        db_output = CompletionDataset(
            name=output_data.name,
            dataset_id=dataset_id,
            completions=output_data.completions,
            user_metadata=output_data.metadata
        )
        self.db.add(db_output)
        self.db.commit()
        self.db.refresh(db_output)
        return db_output
    
    def get_completion_dataset(self, output_id: uuid.UUID) -> Optional[CompletionDataset]:
        """Get an completion dataset by ID."""
        return self.db.query(CompletionDataset).filter(CompletionDataset.id == output_id).first()
    
    def get_completion_datasets(self, dataset_id: uuid.UUID) -> List[CompletionDataset]:
        """Get all completion datasets for a dataset."""
        return (
            self.db.query(CompletionDataset)
            .filter(CompletionDataset.dataset_id == dataset_id)
            .all()
        )