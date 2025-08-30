from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from ..core.database import Base


class CompletionDataset(Base):
    __tablename__ = "completion_datasets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completions = Column(JSON, nullable=False)  # mapping (dataset_name, input_id) -> [output_strings]
    user_metadata = Column('metadata', JSON, default=dict)
    
    # Relationship
    dataset = relationship("Dataset", backref="completion_datasets")