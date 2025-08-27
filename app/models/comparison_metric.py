from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class ComparisonMetric(Base):
    __tablename__ = "comparison_metrics"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comparison_id = Column(UUID(as_uuid=True), ForeignKey("comparisons.id"))
    metric_name = Column(String)  # entropy, token_count, custom_score
    dataset_a_value = Column(Float)
    dataset_b_value = Column(Float)
    statistical_significance = Column(Float)  # p-value
    effect_size = Column(Float)
    confidence_interval_lower = Column(Float)
    confidence_interval_upper = Column(Float)

    created_at = Column(DateTime(timezone=True), server_default=func.now())