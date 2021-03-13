"""migration_2

Revision ID: 3f361790c968
Revises: 475961d7309d
Create Date: 2021-03-13 07:46:28.638536

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f361790c968'
down_revision = '475961d7309d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_messages', sa.Column('recipient_user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'chat_messages', 'users', ['recipient_user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'chat_messages', type_='foreignkey')
    op.drop_column('chat_messages', 'recipient_user_id')
    # ### end Alembic commands ###