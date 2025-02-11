"""initial

Revision ID: 9a8952ad5a02
Revises: 
Create Date: 2025-02-02 20:12:17.638752

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from services.auth import get_password_hash


# revision identifiers, used by Alembic.
revision: str = '9a8952ad5a02'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_stuff', sa.Boolean(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('account',
    sa.Column('balance', sa.Numeric(precision=11, scale=2), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment',
    sa.Column('transaction_id', sa.UUID(), nullable=False),
    sa.Column('amount', sa.Numeric(precision=11, scale=2), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('account_id', sa.UUID(), nullable=False),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.execute(
        f"""
        INSERT INTO public.user (id, first_name, last_name, email, password, is_stuff)
        VALUES ('{uuid4()}', 'Ben', 'Doe', 'ben@gmail.com', '{get_password_hash("123")}', 'f')
        """
    )
    op.execute(
        f"""
        INSERT INTO public.user (id, first_name, last_name, email, password, is_stuff)
        VALUES ('{uuid4()}', 'John', 'Smith', 'john@gmail.com', '{get_password_hash("123")}', 't')
        """
    )    
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('account')
    op.drop_table('user')
    # ### end Alembic commands ###
