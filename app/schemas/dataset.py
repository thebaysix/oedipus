from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class DatasetCreate(BaseModel):
    name: str
    prompts: Dict[str, str]  # mapping inputId -> input_string
    metadata: Optional[Dict[str, Any]] = {}


class DatasetResponse(BaseModel):
    id: uuid.UUID
    name: str
    user_id: uuid.UUID
    created_at: datetime
    prompts: Dict[str, str]
    metadata: Dict[str, Any]

    @classmethod
    def from_orm_with_alias(cls, obj: "Dataset"):
        # Map ORM user_metadata -> API metadata
        return cls(
            id=obj.id,
            name=obj.name,
            user_id=obj.user_id,
            created_at=obj.created_at,
            prompts=obj.prompts,
            metadata=getattr(obj, 'user_metadata', {}) or {}
        )
    
    class Config:
        from_attributes = True