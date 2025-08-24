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
    
    class Config:
        from_attributes = True