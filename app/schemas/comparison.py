from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid


# Keep this request model compatible with the existing frontend.
# It accepts a base dataset_id and a list of output_dataset_ids to compare.
class ComparisonCreate(BaseModel):
    name: str
    dataset_id: uuid.UUID
    output_dataset_ids: List[uuid.UUID] = Field(..., min_items=2, description="At least two output datasets to compare")
    alignment_key: str = "input_id"
    comparison_config: Optional[Dict[str, Any]] = {}


class ComparisonResponse(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime

    # Configuration (as stored on the model per spec)
    datasets: List[uuid.UUID]
    alignment_key: str
    comparison_config: Dict[str, Any]

    # Results
    statistical_results: Dict[str, Any]
    automated_insights: List[str]
    status: str

    class Config:
        from_attributes = True