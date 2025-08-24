from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class AnalysisJobCreate(BaseModel):
    output_dataset_id: uuid.UUID


class AnalysisJobResponse(BaseModel):
    id: uuid.UUID
    output_dataset_id: uuid.UUID
    status: str
    results: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True