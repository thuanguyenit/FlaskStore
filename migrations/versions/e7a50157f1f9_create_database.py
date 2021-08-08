"""create database

Revision ID: e7a50157f1f9
Revises: 
Create Date: 2021-08-08 04:12:05.786609

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7a50157f1f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_index(op.f('ix_category_description'), 'category', ['description'], unique=False)
    op.create_table('product',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(length=64), nullable=False),
    sa.Column('description', sa.String(length=64), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('product_id')
    )
    op.create_index(op.f('ix_product_description'), 'product', ['description'], unique=False)
    op.create_index(op.f('ix_product_product_name'), 'product', ['product_name'], unique=False)
    op.create_index(op.f('ix_product_status'), 'product', ['status'], unique=False)
    op.create_table('product_category',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('product_id', 'category_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('full_name', sa.String(length=64), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=False),
    sa.Column('role', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_full_name'), 'user', ['full_name'], unique=False)
    op.create_table('address',
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('address_id')
    )
    op.create_index(op.f('ix_address_address'), 'address', ['address'], unique=False)
    op.create_table('cart',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'product_id')
    )
    op.create_table('order',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('Status', sa.String(length=64), nullable=False),
    sa.Column('phone', sa.String(length=64), nullable=False),
    sa.Column('address', sa.String(length=64), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_index(op.f('ix_order_Status'), 'order', ['Status'], unique=False)
    op.create_index(op.f('ix_order_address'), 'order', ['address'], unique=False)
    op.create_index(op.f('ix_order_phone'), 'order', ['phone'], unique=False)
    op.create_table('phone',
    sa.Column('phone_id', sa.Integer(), nullable=False),
    sa.Column('phonenumber', sa.String(length=64), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('phone_id')
    )
    op.create_index(op.f('ix_phone_phonenumber'), 'phone', ['phonenumber'], unique=False)
    op.create_table('order_product',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.order_id'], ),
    sa.PrimaryKeyConstraint('order_id', 'product_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_product')
    op.drop_index(op.f('ix_phone_phonenumber'), table_name='phone')
    op.drop_table('phone')
    op.drop_index(op.f('ix_order_phone'), table_name='order')
    op.drop_index(op.f('ix_order_address'), table_name='order')
    op.drop_index(op.f('ix_order_Status'), table_name='order')
    op.drop_table('order')
    op.drop_table('cart')
    op.drop_index(op.f('ix_address_address'), table_name='address')
    op.drop_table('address')
    op.drop_index(op.f('ix_user_full_name'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('product_category')
    op.drop_index(op.f('ix_product_status'), table_name='product')
    op.drop_index(op.f('ix_product_product_name'), table_name='product')
    op.drop_index(op.f('ix_product_description'), table_name='product')
    op.drop_table('product')
    op.drop_index(op.f('ix_category_description'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
