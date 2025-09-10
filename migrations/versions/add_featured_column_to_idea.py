"""Add featured column to idea table

Revision ID: add_featured_to_idea
Revises: 
Create Date: 2025-09-10 22:53:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_featured_to_idea'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add featured column with default value False
    op.add_column('idea', 
        sa.Column('featured', sa.Boolean(), nullable=False, server_default='0')
    )
    # Add index for better performance on featured queries
    op.create_index('idx_idea_featured', 'idea', ['featured'])

def downgrade():
    op.drop_index('idx_idea_featured', table_name='idea')
    op.drop_column('idea', 'featured')
