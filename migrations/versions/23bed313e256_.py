"""empty message

Revision ID: 23bed313e256
Revises: fd0578f758c2
Create Date: 2023-02-25 21:35:21.104671

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23bed313e256'
down_revision = 'fd0578f758c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('blocklist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('exp', sa.DateTime(), nullable=False))

    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('grade',
               existing_type=sa.REAL(),
               type_=sa.Float(precision=2),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('courses', schema=None) as batch_op:
        batch_op.alter_column('grade',
               existing_type=sa.Float(precision=2),
               type_=sa.REAL(),
               existing_nullable=False)

    with op.batch_alter_table('blocklist', schema=None) as batch_op:
        batch_op.drop_column('exp')

    # ### end Alembic commands ###
