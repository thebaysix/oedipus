from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


class ComparisonCreate(BaseModel):
    name: str
    dataset_id: uuid.UUID
    output_dataset_ids: List[uuid.UUID] = Field(..., min_items=2, description="At least two output datasets to compare")
    alignment_key: str = "input_id"
    comparison_config: Optional[Dict[str, Any]] = {}


class AlignmentStats(BaseModel):
    total_inputs: int
    datasets_included: int
    matched_inputs: int
    coverage_percentage: float
    unmatched_inputs: Dict[str, List[str]]  # dataset_id -> list[input_id]


class ComparisonResponse(BaseModel):
    id: uuid.UUID
    name: str
    dataset_id: uuid.UUID
    output_dataset_ids: List[uuid.UUID]
    alignment_key: str
    comparison_config: Dict[str, Any]
    alignment_stats: Dict[str, Any]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True