-- ============================================
-- Schema SQL gerado automaticamente
-- Data: 2026-08-12 02:28:06
-- Total de tabelas: 24
-- ============================================

BEGIN;

-- Tabela gerada a partir do arquivo: addresses.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS addresses CASCADE;

CREATE TABLE addresses (
    id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    address_type VARCHAR(29) NOT NULL,
    postal_code VARCHAR(29) NOT NULL,
    street VARCHAR(55) NOT NULL,
    number INTEGER NOT NULL,
    complement VARCHAR(28) NULL,
    district VARCHAR(53) NOT NULL,
    city VARCHAR(47) NOT NULL,
    state VARCHAR(22) NOT NULL,
    country VARCHAR(22) NOT NULL,
    is_primary BOOLEAN NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE addresses IS 'Dados importados do arquivo addresses.csv';
COMMENT ON COLUMN addresses.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN addresses.customer_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN addresses.address_type IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN addresses.postal_code IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN addresses.street IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(55)';
COMMENT ON COLUMN addresses.number IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN addresses.complement IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(28)';
COMMENT ON COLUMN addresses.district IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(53)';
COMMENT ON COLUMN addresses.city IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(47)';
COMMENT ON COLUMN addresses.state IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN addresses.country IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN addresses.is_primary IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';


-- Tabela gerada a partir do arquivo: attributes.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS attributes CASCADE;

CREATE TABLE attributes (
    id INTEGER NOT NULL,
    name VARCHAR(30) NOT NULL,
    data_type VARCHAR(27) NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE attributes IS 'Dados importados do arquivo attributes.csv';
COMMENT ON COLUMN attributes.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN attributes.name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(30)';
COMMENT ON COLUMN attributes.data_type IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(27)';


-- Tabela gerada a partir do arquivo: brands.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS brands CASCADE;

CREATE TABLE brands (
    id INTEGER NOT NULL,
    name VARCHAR(34) NOT NULL,
    country VARCHAR(22) NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE brands IS 'Dados importados do arquivo brands.csv';
COMMENT ON COLUMN brands.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN brands.name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(34)';
COMMENT ON COLUMN brands.country IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN brands.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN brands.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN brands.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: categories.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS categories CASCADE;

CREATE TABLE categories (
    id INTEGER NOT NULL,
    name VARCHAR(40) NOT NULL,
    slug VARCHAR(40) NOT NULL,
    parent_category_id INTEGER NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE categories IS 'Dados importados do arquivo categories.csv';
COMMENT ON COLUMN categories.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN categories.name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(40)';
COMMENT ON COLUMN categories.slug IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(40)';
COMMENT ON COLUMN categories.parent_category_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN categories.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN categories.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN categories.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: customers.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    id INTEGER NOT NULL,
    person_type VARCHAR(22) NOT NULL,
    legal_name VARCHAR(52) NOT NULL,
    trade_name VARCHAR(47) NULL,
    tax_id BIGINT NOT NULL,
    state_registration VARCHAR(30) NULL,
    email VARCHAR(69) NULL,
    phone VARCHAR(34) NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE customers IS 'Dados importados do arquivo customers.csv';
COMMENT ON COLUMN customers.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN customers.person_type IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN customers.legal_name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(52)';
COMMENT ON COLUMN customers.trade_name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(47)';
COMMENT ON COLUMN customers.tax_id IS 'Coluna gerada automaticamente, tipo inferido: BIGINT';
COMMENT ON COLUMN customers.state_registration IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(30)';
COMMENT ON COLUMN customers.email IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(69)';
COMMENT ON COLUMN customers.phone IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(34)';
COMMENT ON COLUMN customers.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN customers.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN customers.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: employees.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS employees CASCADE;

CREATE TABLE employees (
    id INTEGER NOT NULL,
    full_name VARCHAR(45) NOT NULL,
    cpf BIGINT NOT NULL,
    email VARCHAR(66) NOT NULL,
    role VARCHAR(31) NOT NULL,
    primary_location_id INTEGER NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE employees IS 'Dados importados do arquivo employees.csv';
COMMENT ON COLUMN employees.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN employees.full_name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(45)';
COMMENT ON COLUMN employees.cpf IS 'Coluna gerada automaticamente, tipo inferido: BIGINT';
COMMENT ON COLUMN employees.email IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(66)';
COMMENT ON COLUMN employees.role IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(31)';
COMMENT ON COLUMN employees.primary_location_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN employees.hire_date IS 'Coluna gerada automaticamente, tipo inferido: DATE';
COMMENT ON COLUMN employees.termination_date IS 'Coluna gerada automaticamente, tipo inferido: DATE';
COMMENT ON COLUMN employees.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN employees.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN employees.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: fiscal_invoices.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS fiscal_invoices CASCADE;

CREATE TABLE fiscal_invoices (
    id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    nfe_number VARCHAR(32) NOT NULL,
    nfe_access_key VARCHAR(64) NOT NULL,
    series INTEGER NOT NULL,
    issued_at TIMESTAMP NOT NULL,
    status VARCHAR(30) NOT NULL,
    total_amount DECIMAL(12, 2) NOT NULL,
    xml_storage_uri VARCHAR(89) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE fiscal_invoices IS 'Dados importados do arquivo fiscal_invoices.csv';
COMMENT ON COLUMN fiscal_invoices.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN fiscal_invoices.order_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN fiscal_invoices.nfe_number IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(32)';
COMMENT ON COLUMN fiscal_invoices.nfe_access_key IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(64)';
COMMENT ON COLUMN fiscal_invoices.series IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN fiscal_invoices.issued_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN fiscal_invoices.status IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(30)';
COMMENT ON COLUMN fiscal_invoices.total_amount IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN fiscal_invoices.xml_storage_uri IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(89)';
COMMENT ON COLUMN fiscal_invoices.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN fiscal_invoices.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: goods_receipt_items.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS goods_receipt_items CASCADE;

CREATE TABLE goods_receipt_items (
    id INTEGER NOT NULL,
    goods_receipt_id INTEGER NOT NULL,
    purchase_order_item_id INTEGER NOT NULL,
    quantity_received DECIMAL(12, 2) NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE goods_receipt_items IS 'Dados importados do arquivo goods_receipt_items.csv';
COMMENT ON COLUMN goods_receipt_items.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN goods_receipt_items.goods_receipt_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN goods_receipt_items.purchase_order_item_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN goods_receipt_items.quantity_received IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';


-- Tabela gerada a partir do arquivo: goods_receipts.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS goods_receipts CASCADE;

CREATE TABLE goods_receipts (
    id INTEGER NOT NULL,
    purchase_order_id INTEGER NOT NULL,
    received_by_employee_id INTEGER NOT NULL,
    received_at TIMESTAMP NOT NULL,
    notes VARCHAR(35) NULL,
    created_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE goods_receipts IS 'Dados importados do arquivo goods_receipts.csv';
COMMENT ON COLUMN goods_receipts.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN goods_receipts.purchase_order_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN goods_receipts.received_by_employee_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN goods_receipts.received_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN goods_receipts.notes IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(35)';
COMMENT ON COLUMN goods_receipts.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: locations.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS locations CASCADE;

CREATE TABLE locations (
    id INTEGER NOT NULL,
    name VARCHAR(36) NOT NULL,
    location_type VARCHAR(29) NOT NULL,
    postal_code VARCHAR(29) NOT NULL,
    street VARCHAR(44) NOT NULL,
    number INTEGER NOT NULL,
    complement VARCHAR(27) NULL,
    district VARCHAR(47) NOT NULL,
    city VARCHAR(38) NOT NULL,
    state VARCHAR(22) NOT NULL,
    country VARCHAR(22) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE locations IS 'Dados importados do arquivo locations.csv';
COMMENT ON COLUMN locations.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN locations.name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(36)';
COMMENT ON COLUMN locations.location_type IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN locations.postal_code IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN locations.street IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(44)';
COMMENT ON COLUMN locations.number IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN locations.complement IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(27)';
COMMENT ON COLUMN locations.district IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(47)';
COMMENT ON COLUMN locations.city IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(38)';
COMMENT ON COLUMN locations.state IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN locations.country IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN locations.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN locations.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN locations.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: order_items.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS order_items CASCADE;

CREATE TABLE order_items (
    id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    product_variant_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    icms_rate DECIMAL(12, 2) NOT NULL,
    ipi_rate DECIMAL(12, 2) NOT NULL,
    line_total DECIMAL(12, 2) NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE order_items IS 'Dados importados do arquivo order_items.csv';
COMMENT ON COLUMN order_items.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN order_items.order_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN order_items.product_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN order_items.quantity IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN order_items.unit_price IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN order_items.icms_rate IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN order_items.ipi_rate IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN order_items.line_total IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';


-- Tabela gerada a partir do arquivo: orders.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS orders CASCADE;

CREATE TABLE orders (
    id INTEGER NOT NULL,
    order_number VARCHAR(29) NOT NULL,
    channel VARCHAR(29) NOT NULL,
    customer_id INTEGER NOT NULL,
    salesperson_id INTEGER NULL,
    location_id INTEGER NOT NULL,
    status VARCHAR(29) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    discount_amount DECIMAL(12, 2) NOT NULL,
    total DECIMAL(12, 2) NOT NULL,
    placed_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE orders IS 'Dados importados do arquivo orders.csv';
COMMENT ON COLUMN orders.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN orders.order_number IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN orders.channel IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN orders.customer_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN orders.salesperson_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN orders.location_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN orders.status IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN orders.subtotal IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN orders.discount_amount IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN orders.total IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN orders.placed_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN orders.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN orders.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: payments.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS payments CASCADE;

CREATE TABLE payments (
    id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    method VARCHAR(33) NOT NULL,
    installments INTEGER NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    status VARCHAR(28) NOT NULL,
    paid_at TIMESTAMP NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE payments IS 'Dados importados do arquivo payments.csv';
COMMENT ON COLUMN payments.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN payments.order_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN payments.method IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(33)';
COMMENT ON COLUMN payments.installments IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN payments.amount IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN payments.status IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(28)';
COMMENT ON COLUMN payments.paid_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN payments.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN payments.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: product_suppliers.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS product_suppliers CASCADE;

CREATE TABLE product_suppliers (
    product_variant_id INTEGER NOT NULL,
    supplier_id INTEGER NOT NULL,
    supplier_sku VARCHAR(33) NULL,
    last_quoted_cost DECIMAL(12, 2) NOT NULL,
    lead_time_days INTEGER NOT NULL,
    is_preferred BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE product_suppliers IS 'Dados importados do arquivo product_suppliers.csv';
COMMENT ON COLUMN product_suppliers.product_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN product_suppliers.supplier_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN product_suppliers.supplier_sku IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(33)';
COMMENT ON COLUMN product_suppliers.last_quoted_cost IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN product_suppliers.lead_time_days IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN product_suppliers.is_preferred IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN product_suppliers.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN product_suppliers.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: product_variants.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS product_variants CASCADE;

CREATE TABLE product_variants (
    id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    sku VARCHAR(30) NOT NULL,
    barcode_ean BIGINT NULL,
    sale_price DECIMAL(12, 2) NOT NULL,
    cost_price DECIMAL(12, 2) NOT NULL,
    weight_kg DECIMAL(12, 2) NOT NULL,
    icms_rate DECIMAL(12, 2) NOT NULL,
    ipi_rate DECIMAL(12, 2) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE product_variants IS 'Dados importados do arquivo product_variants.csv';
COMMENT ON COLUMN product_variants.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN product_variants.product_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN product_variants.sku IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(30)';
COMMENT ON COLUMN product_variants.barcode_ean IS 'Coluna gerada automaticamente, tipo inferido: BIGINT';
COMMENT ON COLUMN product_variants.sale_price IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN product_variants.cost_price IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN product_variants.weight_kg IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN product_variants.icms_rate IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN product_variants.ipi_rate IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN product_variants.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN product_variants.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN product_variants.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: products.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE products (
    id INTEGER NOT NULL,
    name VARCHAR(43) NOT NULL,
    description VARCHAR(68) NULL,
    brand_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    ncm_code INTEGER NOT NULL,
    unit_of_measure VARCHAR(22) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE products IS 'Dados importados do arquivo products.csv';
COMMENT ON COLUMN products.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN products.name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(43)';
COMMENT ON COLUMN products.description IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(68)';
COMMENT ON COLUMN products.brand_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN products.category_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN products.ncm_code IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN products.unit_of_measure IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN products.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN products.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN products.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: purchase_order_items.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS purchase_order_items CASCADE;

CREATE TABLE purchase_order_items (
    id INTEGER NOT NULL,
    purchase_order_id INTEGER NOT NULL,
    product_variant_id INTEGER NOT NULL,
    quantity_ordered INTEGER NOT NULL,
    unit_cost DECIMAL(12, 2) NOT NULL,
    line_total DECIMAL(12, 2) NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE purchase_order_items IS 'Dados importados do arquivo purchase_order_items.csv';
COMMENT ON COLUMN purchase_order_items.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_order_items.purchase_order_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_order_items.product_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_order_items.quantity_ordered IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_order_items.unit_cost IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN purchase_order_items.line_total IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';


-- Tabela gerada a partir do arquivo: purchase_orders.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS purchase_orders CASCADE;

CREATE TABLE purchase_orders (
    id INTEGER NOT NULL,
    po_number VARCHAR(29) NOT NULL,
    supplier_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    destination_location_id INTEGER NOT NULL,
    status VARCHAR(38) NOT NULL,
    currency VARCHAR(23) NOT NULL,
    subtotal DECIMAL(12, 2) NOT NULL,
    total DECIMAL(12, 2) NOT NULL,
    placed_at TIMESTAMP NOT NULL,
    expected_delivery_at DATE NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE purchase_orders IS 'Dados importados do arquivo purchase_orders.csv';
COMMENT ON COLUMN purchase_orders.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_orders.po_number IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN purchase_orders.supplier_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_orders.buyer_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_orders.destination_location_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN purchase_orders.status IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(38)';
COMMENT ON COLUMN purchase_orders.currency IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(23)';
COMMENT ON COLUMN purchase_orders.subtotal IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN purchase_orders.total IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN purchase_orders.placed_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN purchase_orders.expected_delivery_at IS 'Coluna gerada automaticamente, tipo inferido: DATE';
COMMENT ON COLUMN purchase_orders.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN purchase_orders.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: return_items.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS return_items CASCADE;

CREATE TABLE return_items (
    id INTEGER NOT NULL,
    return_id INTEGER NOT NULL,
    order_item_id INTEGER NOT NULL,
    quantity DECIMAL(12, 2) NOT NULL,
    action VARCHAR(28) NOT NULL,
    exchange_variant_id INTEGER NULL,
    unit_refund_amount DECIMAL(12, 2) NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE return_items IS 'Dados importados do arquivo return_items.csv';
COMMENT ON COLUMN return_items.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN return_items.return_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN return_items.order_item_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN return_items.quantity IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN return_items.action IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(28)';
COMMENT ON COLUMN return_items.exchange_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN return_items.unit_refund_amount IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';


-- Tabela gerada a partir do arquivo: returns.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS returns CASCADE;

CREATE TABLE returns (
    id INTEGER NOT NULL,
    return_number VARCHAR(29) NOT NULL,
    order_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    received_at_location_id INTEGER NOT NULL,
    status VARCHAR(29) NOT NULL,
    reason VARCHAR(53) NULL,
    total_refund_amount DECIMAL(12, 2) NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE returns IS 'Dados importados do arquivo returns.csv';
COMMENT ON COLUMN returns.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN returns.return_number IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN returns.order_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN returns.customer_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN returns.received_at_location_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN returns.status IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(29)';
COMMENT ON COLUMN returns.reason IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(53)';
COMMENT ON COLUMN returns.total_refund_amount IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN returns.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN returns.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: stock_levels.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS stock_levels CASCADE;

CREATE TABLE stock_levels (
    product_variant_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    quantity_on_hand DECIMAL(12, 2) NOT NULL,
    reorder_point TEXT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE stock_levels IS 'Dados importados do arquivo stock_levels.csv';
COMMENT ON COLUMN stock_levels.product_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_levels.location_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_levels.quantity_on_hand IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN stock_levels.reorder_point IS 'Coluna gerada automaticamente, tipo inferido: TEXT';
COMMENT ON COLUMN stock_levels.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: stock_movements.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS stock_movements CASCADE;

CREATE TABLE stock_movements (
    id INTEGER NOT NULL,
    product_variant_id INTEGER NOT NULL,
    location_id INTEGER NOT NULL,
    movement_type VARCHAR(31) NOT NULL,
    quantity DECIMAL(12, 2) NOT NULL,
    reference_table VARCHAR(34) NULL,
    reference_id INTEGER NULL,
    employee_id INTEGER NULL,
    notes VARCHAR(54) NULL,
    occurred_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE stock_movements IS 'Dados importados do arquivo stock_movements.csv';
COMMENT ON COLUMN stock_movements.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_movements.product_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_movements.location_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_movements.movement_type IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(31)';
COMMENT ON COLUMN stock_movements.quantity IS 'Coluna gerada automaticamente, tipo inferido: DECIMAL(12, 2)';
COMMENT ON COLUMN stock_movements.reference_table IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(34)';
COMMENT ON COLUMN stock_movements.reference_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_movements.employee_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN stock_movements.notes IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(54)';
COMMENT ON COLUMN stock_movements.occurred_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN stock_movements.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: suppliers.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS suppliers CASCADE;

CREATE TABLE suppliers (
    id INTEGER NOT NULL,
    legal_name VARCHAR(50) NOT NULL,
    trade_name VARCHAR(31) NULL,
    country VARCHAR(22) NOT NULL,
    tax_id VARCHAR(34) NOT NULL,
    tax_id_type VARCHAR(24) NOT NULL,
    email VARCHAR(50) NOT NULL,
    phone BIGINT NOT NULL,
    contact_name VARCHAR(47) NOT NULL,
    is_active BOOLEAN NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL

);

-- Comentários da tabela:
COMMENT ON TABLE suppliers IS 'Dados importados do arquivo suppliers.csv';
COMMENT ON COLUMN suppliers.id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN suppliers.legal_name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(50)';
COMMENT ON COLUMN suppliers.trade_name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(31)';
COMMENT ON COLUMN suppliers.country IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(22)';
COMMENT ON COLUMN suppliers.tax_id IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(34)';
COMMENT ON COLUMN suppliers.tax_id_type IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(24)';
COMMENT ON COLUMN suppliers.email IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(50)';
COMMENT ON COLUMN suppliers.phone IS 'Coluna gerada automaticamente, tipo inferido: BIGINT';
COMMENT ON COLUMN suppliers.contact_name IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(47)';
COMMENT ON COLUMN suppliers.is_active IS 'Coluna gerada automaticamente, tipo inferido: BOOLEAN';
COMMENT ON COLUMN suppliers.created_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';
COMMENT ON COLUMN suppliers.updated_at IS 'Coluna gerada automaticamente, tipo inferido: TIMESTAMP';


-- Tabela gerada a partir do arquivo: variant_attribute_values.csv
-- Data de geração: 2026-08-12 02:28:06
-- Schema inferido automaticamente

DROP TABLE IF EXISTS variant_attribute_values CASCADE;

CREATE TABLE variant_attribute_values (
    product_variant_id INTEGER NOT NULL,
    attribute_id INTEGER NOT NULL,
    value VARCHAR(34) NULL

);

-- Comentários da tabela:
COMMENT ON TABLE variant_attribute_values IS 'Dados importados do arquivo variant_attribute_values.csv';
COMMENT ON COLUMN variant_attribute_values.product_variant_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN variant_attribute_values.attribute_id IS 'Coluna gerada automaticamente, tipo inferido: INTEGER';
COMMENT ON COLUMN variant_attribute_values.value IS 'Coluna gerada automaticamente, tipo inferido: VARCHAR(34)';

COMMIT;

-- ============================================
-- Fim do arquivo de schema
-- Verifique os tipos inferidos antes de executar em produção
-- ============================================