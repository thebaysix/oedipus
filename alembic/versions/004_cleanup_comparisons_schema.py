"""Cleanup comparisons schema: drop legacy columns, ensure new columns

Revision ID: 004
Revises: 003
Create Date: 2025-08-27 00:35:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Ensure new columns exist
    conn.execute(sa.text("""
        ALTER TABLE IF EXISTS comparisons
        ADD COLUMN IF NOT EXISTS datasets JSON,
        ADD COLUMN IF NOT EXISTS statistical_results JSON,
        ADD COLUMN IF NOT EXISTS automated_insights JSON;
    """))

    # Drop legacy columns if present (CASCADE to remove dependent constraints)
    conn.execute(sa.text("""
        ALTER TABLE IF EXISTS comparisons
        DROP COLUMN IF EXISTS alignment_stats CASCADE,
        DROP COLUMN IF EXISTS completion_dataset_ids CASCADE,
        DROP COLUMN IF EXISTS dataset_id CASCADE;
    """))


def downgrade() -> None:
    # Downgrade is best-effort; recreate legacy columns as nullable for compatibility
    conn = op.get_bind()
    conn.execute(sa.text("""
        ALTER TABLE IF EXISTS comparisons
        ADD COLUMN IF NOT EXISTS dataset_id UUID,
        ADD COLUMN IF NOT EXISTS completion_dataset_ids JSON,
        ADD COLUMN IF NOT EXISTS alignment_stats JSON;
    """))