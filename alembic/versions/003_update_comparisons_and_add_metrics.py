"""Update comparisons schema and add comparison_metrics

Revision ID: 003
Revises: 002
Create Date: 2025-08-27 00:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to comparisons per spec
    with op.batch_alter_table('comparisons') as batch_op:
        batch_op.add_column(sa.Column('datasets', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('statistical_results', sa.JSON(), nullable=True))
        batch_op.add_column(sa.Column('automated_insights', sa.JSON(), nullable=True))
        # status column already exists; keep as-is
        # alignment_key and comparison_config already exist from 002; keep as-is

    # Backfill datasets from legacy columns if available
    conn = op.get_bind()
    try:
        conn.execute(sa.text(
            """
            UPDATE comparisons
            SET datasets = (
                (json_build_array(dataset_id)::jsonb) || COALESCE(completion_dataset_ids::jsonb, '[]'::jsonb)
            )::json
            WHERE datasets IS NULL
            """
        ))
    except Exception:
        # Best-effort backfill; ignore if columns don't exist (fresh DB)
        pass

    # Drop legacy columns that are no longer used to avoid NOT NULL enforcement
    try:
        with op.batch_alter_table('comparisons') as batch_op:
            # Drop alignment_stats if exists
            try:
                batch_op.drop_column('alignment_stats')
            except Exception:
                pass
            # Drop completion_dataset_ids and dataset_id to match new model
            try:
                batch_op.drop_column('completion_dataset_ids')
            except Exception:
                pass
            try:
                batch_op.drop_column('dataset_id')
            except Exception:
                pass
    except Exception:
        # In case of fresh DB or already applied changes, continue
        pass

    # Create comparison_metrics table if not exists
    conn = op.get_bind()
    res = conn.execute(sa.text("""
        SELECT to_regclass('public.comparison_metrics') IS NOT NULL AS exists;
    """))
    exists = list(res)[0][0]
    if not exists:
        op.create_table(
            'comparison_metrics',
            sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
            sa.Column('comparison_id', postgresql.UUID(as_uuid=True), nullable=True),
            sa.Column('metric_name', sa.String(), nullable=True),
            sa.Column('dataset_a_value', sa.Float(), nullable=True),
            sa.Column('dataset_b_value', sa.Float(), nullable=True),
            sa.Column('statistical_significance', sa.Float(), nullable=True),
            sa.Column('effect_size', sa.Float(), nullable=True),
            sa.Column('confidence_interval_lower', sa.Float(), nullable=True),
            sa.Column('confidence_interval_upper', sa.Float(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.ForeignKeyConstraint(['comparison_id'], ['comparisons.id']),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade() -> None:
    # Drop comparison_metrics
    op.drop_table('comparison_metrics')

    # Remove added columns from comparisons
    with op.batch_alter_table('comparisons') as batch_op:
        batch_op.drop_column('automated_insights')
        batch_op.drop_column('statistical_results')
        batch_op.drop_column('datasets')