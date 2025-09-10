"""Add newsletter subscribers table

Revision ID: add_newsletter_subscribers_table
Revises: 
Create Date: 2025-09-10 22:51:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_newsletter_subscribers_table'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create newsletter_subscribers table
    op.create_table('newsletter_subscribers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='1'),
        sa.Column('subscribed_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('unsubscribed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

def downgrade():
    op.drop_table('newsletter_subscribers')
