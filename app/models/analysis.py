from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    output_dataset_id = Column(UUID(as_uuid=True), ForeignKey("output_datasets.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")  # pending/running/completed/failed
    results = Column(JSON, default=dict)  # computed metrics
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    output_dataset = relationship("OutputDataset", backref="analysis_jobs")