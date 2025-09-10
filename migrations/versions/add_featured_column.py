"""Add featured column to Idea

Revision ID: add_featured_column
Revises: 
Create Date: 2025-09-10 22:38:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_featured_column'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('idea', sa.Column('featured', sa.Boolean(), nullable=True, default=False))

def downgrade():
    op.drop_column('idea', 'featured')
