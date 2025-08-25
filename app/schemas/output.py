from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid


class OutputDatasetCreate(BaseModel):
    name: str
    outputs: Dict[str, List[str]]  # mapping input_id -> [output_strings]
    metadata: Optional[Dict[str, Any]] = {}


class OutputDatasetResponse(BaseModel):
    id: uuid.UUID
    name: str
    dataset_id: uuid.UUID
    created_at: datetime
    outputs: Dict[str, List[str]]
    metadata: Dict[str, Any]

    @classmethod
    def from_orm_with_alias(cls, obj: "OutputDataset"):
        # Map ORM user_metadata -> API metadata
        return cls(
            id=obj.id,
            name=obj.name,
            dataset_id=obj.dataset_id,
            created_at=obj.created_at,
            outputs=obj.outputs,
            metadata=getattr(obj, 'user_metadata', {}) or {}
        )
    
    class Config:
        from_attributes = True