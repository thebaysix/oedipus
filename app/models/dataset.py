from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..core.database import Base


class Dataset(Base):
    __tablename__ = "datasets"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    inputs = Column(JSON, nullable=False)  # mapping inputId -> input_string
    user_metadata = Column('metadata', JSON, default=dict)  # user-defined metadata