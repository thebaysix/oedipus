from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid
from ..core.database import Base


class Comparison(Base):
    __tablename__ = "comparisons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Configuration
    datasets = Column(JSON)  # References to existing datasets (UUIDs as strings)
    alignment_key = Column(String, default="input_id")
    comparison_config = Column(JSON)  # User preferences, thresholds

    # Results
    statistical_results = Column(JSON)  # Test outcomes, p-values, effect sizes (also holds alignment summary in Phase 1)
    automated_insights = Column(JSON)  # List[str]
    status = Column(String, default="pending")  # pending/running/completed/failed