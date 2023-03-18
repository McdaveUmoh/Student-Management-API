"""empty message

Revision ID: af4da17c1dd9
Revises: a3f4ca11c8ba
Create Date: 2023-03-17 12:40:44.864643

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af4da17c1dd9'
down_revision = 'a3f4ca11c8ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_type', sa.String(length=20), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('teachers', schema=None) as batch_op:
        batch_op.drop_column('user_type')

    op.drop_table('admin')
    # ### end Alembic commands ###
