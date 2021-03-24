"""update

Revision ID: 95006bda00db
Revises: d0eda29ada4e
Create Date: 2021-03-24 01:47:31.650045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95006bda00db'
down_revision = 'd0eda29ada4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_notifications', sa.Column('recipient_user_id', sa.Integer(), nullable=False))
    op.drop_constraint('chat_notifications_sender_user_id_fkey', 'chat_notifications', type_='foreignkey')
    op.drop_constraint('chat_notifications_user_connection_id_fkey', 'chat_notifications', type_='foreignkey')
    op.create_foreign_key(None, 'chat_notifications', 'users', ['recipient_user_id'], ['id'])
    op.drop_column('chat_notifications', 'sender_user_id')
    op.drop_column('chat_notifications', 'user_connection_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chat_notifications', sa.Column('user_connection_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('chat_notifications', sa.Column('sender_user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'chat_notifications', type_='foreignkey')
    op.create_foreign_key('chat_notifications_user_connection_id_fkey', 'chat_notifications', 'user_connections', ['user_connection_id'], ['id'])
    op.create_foreign_key('chat_notifications_sender_user_id_fkey', 'chat_notifications', 'users', ['sender_user_id'], ['id'])
    op.drop_column('chat_notifications', 'recipient_user_id')
    # ### end Alembic commands ###
