from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class DatasetCreate(BaseModel):
    name: str
    inputs: Dict[str, str]  # mapping inputId -> input_string
    metadata: Optional[Dict[str, Any]] = {}


class DatasetResponse(BaseModel):
    id: uuid.UUID
    name: str
    user_id: uuid.UUID
    created_at: datetime
    inputs: Dict[str, str]
    metadata: Dict[str, Any]
    
    class Config:
        from_attributes = True