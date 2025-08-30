"""rename inputs column to prompts

Revision ID: 9399fb9b214b
Revises: 004
Create Date: 2025-08-29 23:13:08.212102

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9399fb9b214b'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename the 'inputs' column to 'prompts' in the datasets table
    op.alter_column('datasets', 'inputs', new_column_name='prompts')


def downgrade() -> None:
    # Rename the 'prompts' column back to 'inputs' in the datasets table
    op.alter_column('datasets', 'prompts', new_column_name='inputs')