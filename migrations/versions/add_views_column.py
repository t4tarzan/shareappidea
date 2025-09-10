"""Add views column to Idea

Revision ID: add_views_column
Revises: 
Create Date: 2025-09-10 22:45:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_views_column'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('idea', sa.Column('views', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('idea', 'views')
