"""Add comparisons table

Revision ID: 002
Revises: 001
Create Date: 2025-08-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'comparisons',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('dataset_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('output_dataset_ids', sa.JSON(), nullable=False),
        sa.Column('alignment_key', sa.String(), nullable=False),
        sa.Column('comparison_config', sa.JSON(), nullable=True),
        sa.Column('alignment_stats', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['dataset_id'], ['datasets.id']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('comparisons')