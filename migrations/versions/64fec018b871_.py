"""empty message

Revision ID: 64fec018b871
Revises: abc9bb5b1944
Create Date: 2021-05-04 16:31:02.785119

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64fec018b871'
down_revision = 'abc9bb5b1944'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ItemCategory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('contact_person', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('item_code', sa.String(), nullable=True),
    sa.Column('serial', sa.String(), nullable=True),
    sa.Column('brand', sa.String(), nullable=True),
    sa.Column('model', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('unit_price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column('stock_in', sa.Integer(), nullable=True),
    sa.Column('stock_out', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['ItemCategory.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['Supplier.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('Inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('number', sa.String(), nullable=False),
    sa.Column('request_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['request_id'], ['Request.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('InventoryItem',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('inventory_id', sa.Integer(), nullable=False),
    sa.Column('request_item_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('purchased_date', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['request_item_id'], ['RequestLine.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Release',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('request_item_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('department_id', sa.Integer(), nullable=True),
    sa.Column('release_date', sa.Date(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('remarks', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['department_id'], ['Department.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['Item.id'], ),
    sa.ForeignKeyConstraint(['request_item_id'], ['RequestLine.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Release')
    op.drop_table('InventoryItem')
    op.drop_table('Inventory')
    op.drop_table('Item')
    op.drop_table('Supplier')
    op.drop_table('ItemCategory')
    # ### end Alembic commands ###