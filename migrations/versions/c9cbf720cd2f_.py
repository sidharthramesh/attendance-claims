"""empty message

Revision ID: c9cbf720cd2f
Revises: 049d12c67e00
Create Date: 2017-04-10 17:29:26.364394

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9cbf720cd2f'
down_revision = '049d12c67e00'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('claim', sa.Column('event_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'claim', 'event', ['event_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'claim', type_='foreignkey')
    op.drop_column('claim', 'event_id')
    op.drop_table('event')
    # ### end Alembic commands ###
