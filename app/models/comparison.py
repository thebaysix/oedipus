from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    # Parent input dataset for which outputs are compared
    dataset_id = Column(UUID(as_uuid=True), ForeignKey("datasets.id"), nullable=False)

    # Configuration
    output_dataset_ids = Column(JSON, nullable=False)  # List[UUID] as JSON array
    alignment_key = Column(String, nullable=False, default="input_id")
    comparison_config = Column(JSON, default=dict)

    # Results/validation
    alignment_stats = Column(JSON, default=dict)
    status = Column(String, nullable=False, default="created")  # created/running/completed/failed

    created_at = Column(DateTime(timezone=True), server_default=func.now())