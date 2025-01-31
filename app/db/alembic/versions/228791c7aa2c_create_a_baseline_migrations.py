"""Create a baseline migrations

Revision ID: 228791c7aa2c
Revises: 
Create Date: 2025-01-31 10:34:42.162921

"""
# pylint: skip-file

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '228791c7aa2c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invoice_sequence',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('invoice_prefix', sa.VARCHAR(length=256), nullable=False),
    sa.Column('last_sequence_number', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invoice_sequence')
    # ### end Alembic commands ###
