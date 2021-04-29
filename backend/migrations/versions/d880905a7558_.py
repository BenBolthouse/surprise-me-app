"""empty message

Revision ID: d880905a7558
Revises: 
Create Date: 2021-04-27 20:12:12.576785

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd880905a7558'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=64), nullable=False),
    sa.Column('last_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('connections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('requestor', sa.Integer(), nullable=False),
    sa.Column('recipient', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('approved_at', sa.DateTime(), nullable=True),
    sa.Column('expired_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['recipient'], ['users.id'], ),
    sa.ForeignKeyConstraint(['requestor'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('email_addresses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('expired_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('seen_at', sa.DateTime(), nullable=True),
    sa.Column('dismissed_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('passwords',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user', sa.Integer(), nullable=False),
    sa.Column('hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('expired_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('passwords')
    op.drop_table('notifications')
    op.drop_table('email_addresses')
    op.drop_table('connections')
    op.drop_table('users')
    # ### end Alembic commands ###