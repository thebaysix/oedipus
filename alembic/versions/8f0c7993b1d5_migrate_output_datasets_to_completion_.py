"""migrate output_datasets to completion_datasets

Revision ID: 8f0c7993b1d5
Revises: 9399fb9b214b
Create Date: 2025-08-30 11:30:44.470531

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f0c7993b1d5'
down_revision = '9399fb9b214b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Step 1: Migrate data from output_datasets to completion_datasets
    # First, rename the 'outputs' column to 'completions' in output_datasets
    op.alter_column('output_datasets', 'outputs', new_column_name='completions')
    
    # Step 2: Insert data from output_datasets into completion_datasets
    op.execute("""
        INSERT INTO completion_datasets (id, name, dataset_id, created_at, completions, metadata)
        SELECT id, name, dataset_id, created_at, completions, metadata
        FROM output_datasets
        WHERE id NOT IN (SELECT id FROM completion_datasets)
    """)
    
    # Step 3: Update analysis_jobs to reference completion_datasets
    # First rename the column
    op.alter_column('analysis_jobs', 'output_dataset_id', new_column_name='completion_dataset_id')
    
    # Drop the old foreign key constraint
    op.drop_constraint('analysis_jobs_output_dataset_id_fkey', 'analysis_jobs', type_='foreignkey')
    
    # Add the new foreign key constraint
    op.create_foreign_key(
        'analysis_jobs_completion_dataset_id_fkey',
        'analysis_jobs', 'completion_datasets',
        ['completion_dataset_id'], ['id']
    )
    
    # Step 4: Drop the old output_datasets table
    op.drop_table('output_datasets')


def downgrade() -> None:
    # This is a complex migration, downgrade would be difficult
    # For now, just raise an error
    raise NotImplementedError("Downgrade not supported for this migration")