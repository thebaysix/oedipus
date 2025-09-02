from pydantic import BaseModel
from typing import Literal
import uuid


class ExportRequest(BaseModel):
    comparison_id: uuid.UUID
    format: Literal['json', 'csv', 'pdf', 'summary']
    include_raw_data: bool = False
    include_statistics: bool = True
    include_insights: bool = True
    include_visualizations: bool = False


class ExportResponse(BaseModel):
    filename: str
    content_type: str
    size_bytes: int