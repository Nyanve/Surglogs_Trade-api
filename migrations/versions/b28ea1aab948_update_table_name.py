"""Update <table_name>

Revision ID: b28ea1aab948
Revises: aee185ea09a5
Create Date: 2023-06-20 18:13:20.355516

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b28ea1aab948'
down_revision = 'aee185ea09a5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Liked',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cur_shortcut', sa.String(length=3), nullable=False),
    sa.Column('exchange_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['exchange_id'], ['user_log.exchange_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Liked')
    # ### end Alembic commands ###