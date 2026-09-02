"""Initial schema creation

Revision ID: 001_initial_schema
Revises: 
Create Date: 2024-09-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create initial database schema"""
    
    # Create enum types
    op.execute("CREATE TYPE transaction_type AS ENUM ('PURCHASE', 'CONSUMPTION', 'ADJUSTMENT', 'WASTE', 'RETURN')")
    op.execute("CREATE TYPE order_status AS ENUM ('QUOTE', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED')")
    op.execute("CREATE TYPE component_type AS ENUM ('SPONGE', 'FILLING', 'FROSTING', 'DECORATION', 'PACKAGING')")
    op.execute("CREATE TYPE activity AS ENUM ('PREP', 'BAKING', 'FILLING', 'FROSTING', 'DECORATION', 'CLEANUP')")
    op.execute("CREATE TYPE cost_type AS ENUM ('FIXED_PER_ORDER', 'USAGE_BASED')")
    op.execute("CREATE TYPE payment_method AS ENUM ('CASH', 'CARD')")
    
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hourly_rate', sa.Numeric(10, 2), nullable=False, server_default='20.00'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.Index('ix_users_email', 'email')
    )
    
    # Customers table
    op.create_table(
        'customers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(20), nullable=True),
        sa.Column('address', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_customers_name', 'name'),
        sa.Index('ix_customers_email', 'email')
    )
    
    # Ingredients table
    op.create_table(
        'ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('base_unit', sa.String(20), nullable=False),
        sa.Column('current_cost_per_unit', sa.Numeric(10, 4), nullable=False),
        sa.Column('current_quantity', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('min_threshold', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('supplier', sa.String(255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.Index('ix_ingredients_name', 'name'),
        sa.Index('ix_ingredients_active', 'active')
    )
    
    # IngredientUnits table
    op.create_table(
        'ingredient_units',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('unit_name', sa.String(50), nullable=False),
        sa.Column('conversion_to_base', sa.Numeric(12, 4), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_ingredient_units_ingredient_id', 'ingredient_id')
    )
    
    # InventoryTransactions table
    op.create_table(
        'inventory_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('transaction_type', sa.Enum('PURCHASE', 'CONSUMPTION', 'ADJUSTMENT', 'WASTE', 'RETURN', name='transaction_type'), nullable=False),
        sa.Column('quantity_change', sa.Numeric(12, 2), nullable=False),
        sa.Column('transaction_date', sa.Date(), nullable=False),
        sa.Column('purchase_price_per_unit', sa.Numeric(10, 4), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_inventory_transactions_ingredient_id', 'ingredient_id'),
        sa.Index('ix_inventory_transactions_transaction_type', 'transaction_type'),
        sa.Index('ix_inventory_transactions_transaction_date', 'transaction_date')
    )
    
    # CakeSupplies table
    op.create_table(
        'cake_supplies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('unit', sa.String(20), nullable=False),
        sa.Column('current_cost_per_unit', sa.Numeric(10, 4), nullable=False),
        sa.Column('current_quantity', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('min_threshold', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('supplier', sa.String(255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.Index('ix_cake_supplies_name', 'name'),
        sa.Index('ix_cake_supplies_active', 'active')
    )
    
    # SupplyTransactions table
    op.create_table(
        'supply_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('supply_id', sa.Integer(), nullable=False),
        sa.Column('transaction_type', sa.Enum('PURCHASE', 'CONSUMPTION', 'ADJUSTMENT', 'WASTE', 'RETURN', name='transaction_type'), nullable=False),
        sa.Column('quantity_change', sa.Numeric(12, 2), nullable=False),
        sa.Column('transaction_date', sa.Date(), nullable=False),
        sa.Column('purchase_price_per_unit', sa.Numeric(10, 4), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['supply_id'], ['cake_supplies.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_supply_transactions_supply_id', 'supply_id'),
        sa.Index('ix_supply_transactions_transaction_type', 'transaction_type'),
        sa.Index('ix_supply_transactions_transaction_date', 'transaction_date')
    )
    
    # Recipes table
    op.create_table(
        'recipes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_recipes_name', 'name'),
        sa.Index('ix_recipes_active', 'active')
    )
    
    # RecipeVariants table
    op.create_table(
        'recipe_variants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_id', sa.Integer(), nullable=False),
        sa.Column('variant_name', sa.String(255), nullable=False),
        sa.Column('base_yield', sa.Numeric(8, 2), nullable=False),
        sa.Column('yield_unit', sa.String(50), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_recipe_variants_recipe_id', 'recipe_id')
    )
    
    # RecipeIngredients table
    op.create_table(
        'recipe_ingredients',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('recipe_variant_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('quantity_required', sa.Numeric(12, 2), nullable=False),
        sa.Column('unit', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.ForeignKeyConstraint(['recipe_variant_id'], ['recipe_variants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_recipe_ingredients_recipe_variant_id', 'recipe_variant_id'),
        sa.Index('ix_recipe_ingredients_ingredient_id', 'ingredient_id')
    )
    
    # Orders table
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_id', sa.Integer(), nullable=False),
        sa.Column('order_date', sa.Date(), nullable=False),
        sa.Column('delivery_date', sa.Date(), nullable=False),
        sa.Column('status', sa.Enum('QUOTE', 'CONFIRMED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED', name='order_status'), nullable=False, server_default='QUOTE'),
        sa.Column('selling_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('discount_amount', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('tax_rate', sa.Numeric(5, 2), nullable=False, server_default='0'),
        sa.Column('tax_amount', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('deposit_amount', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('amount_paid', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('amount_remaining', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('estimated_total_cost', sa.Numeric(10, 2), nullable=False),
        sa.Column('actual_total_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_orders_customer_id', 'customer_id'),
        sa.Index('ix_orders_order_date', 'order_date'),
        sa.Index('ix_orders_status', 'status')
    )
    
    # OrderComponents table
    op.create_table(
        'order_components',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('component_type', sa.Enum('SPONGE', 'FILLING', 'FROSTING', 'DECORATION', 'PACKAGING', name='component_type'), nullable=False),
        sa.Column('recipe_variant_id', sa.Integer(), nullable=True),
        sa.Column('quantity', sa.Numeric(8, 2), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['recipe_variant_id'], ['recipe_variants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_order_components_order_id', 'order_id')
    )
    
    # OrderIngredientUsages table
    op.create_table(
        'order_ingredient_usages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_id', sa.Integer(), nullable=False),
        sa.Column('estimated_quantity', sa.Numeric(12, 2), nullable=False),
        sa.Column('estimated_cost', sa.Numeric(10, 2), nullable=False),
        sa.Column('actual_quantity', sa.Numeric(12, 2), nullable=True),
        sa.Column('actual_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('unit_used', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['ingredient_id'], ['ingredients.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_order_ingredient_usages_order_id', 'order_id'),
        sa.Index('ix_order_ingredient_usages_ingredient_id', 'ingredient_id')
    )
    
    # OrderSupplyUsages table
    op.create_table(
        'order_supply_usages',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('supply_id', sa.Integer(), nullable=False),
        sa.Column('estimated_quantity', sa.Numeric(12, 2), nullable=False),
        sa.Column('estimated_cost', sa.Numeric(10, 2), nullable=False),
        sa.Column('actual_quantity', sa.Numeric(12, 2), nullable=True),
        sa.Column('actual_cost', sa.Numeric(10, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.ForeignKeyConstraint(['supply_id'], ['cake_supplies.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_order_supply_usages_order_id', 'order_id'),
        sa.Index('ix_order_supply_usages_supply_id', 'supply_id')
    )
    
    # LaborEntries table
    op.create_table(
        'labor_entries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('activity', sa.Enum('PREP', 'BAKING', 'FILLING', 'FROSTING', 'DECORATION', 'CLEANUP', name='activity'), nullable=False),
        sa.Column('estimated_minutes', sa.Integer(), nullable=False),
        sa.Column('actual_minutes', sa.Integer(), nullable=True),
        sa.Column('hourly_rate', sa.Numeric(10, 2), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_labor_entries_order_id', 'order_id')
    )
    
    # OperatingCostCategories table
    op.create_table(
        'operating_cost_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cost_type', sa.Enum('FIXED_PER_ORDER', 'USAGE_BASED', name='cost_type'), nullable=False),
        sa.Column('default_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.Index('ix_operating_cost_categories_name', 'name'),
        sa.Index('ix_operating_cost_categories_active', 'active')
    )
    
    # OrderOperatingCosts table
    op.create_table(
        'order_operating_costs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('operating_cost_category_id', sa.Integer(), nullable=False),
        sa.Column('estimated_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('actual_amount', sa.Numeric(10, 2), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['operating_cost_category_id'], ['operating_cost_categories.id'], ),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.Index('ix_order_operating_costs_order_id', 'order_id'),
        sa.Index('ix_order_operating_costs_operating_cost_category_id', 'operating_cost_category_id')
    )
    
    # OrderCostSummaries table
    op.create_table(
        'order_cost_summaries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.Integer(), nullable=False),
        sa.Column('ingredient_cost_estimated', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('ingredient_cost_actual', sa.Numeric(10, 2), nullable=True),
        sa.Column('supply_cost_estimated', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('supply_cost_actual', sa.Numeric(10, 2), nullable=True),
        sa.Column('labor_cost_estimated', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('labor_cost_actual', sa.Numeric(10, 2), nullable=True),
        sa.Column('operating_cost_estimated', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('operating_cost_actual', sa.Numeric(10, 2), nullable=True),
        sa.Column('total_cost_estimated', sa.Numeric(10, 2), nullable=False, server_default='0'),
        sa.Column('total_cost_actual', sa.Numeric(10, 2), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_id')
    )


def downgrade() -> None:
    """Drop all tables"""
    op.drop_table('order_cost_summaries')
    op.drop_table('order_operating_costs')
    op.drop_table('operating_cost_categories')
    op.drop_table('labor_entries')
    op.drop_table('order_supply_usages')
    op.drop_table('order_ingredient_usages')
    op.drop_table('order_components')
    op.drop_table('orders')
    op.drop_table('recipe_ingredients')
    op.drop_table('recipe_variants')
    op.drop_table('recipes')
    op.drop_table('supply_transactions')
    op.drop_table('cake_supplies')
    op.drop_table('inventory_transactions')
    op.drop_table('ingredient_units')
    op.drop_table('ingredients')
    op.drop_table('customers')
    op.drop_table('users')
    
    # Drop enum types
    op.execute("DROP TYPE payment_method")
    op.execute("DROP TYPE cost_type")
    op.execute("DROP TYPE activity")
    op.execute("DROP TYPE component_type")
    op.execute("DROP TYPE order_status")
    op.execute("DROP TYPE transaction_type")
