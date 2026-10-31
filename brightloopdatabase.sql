create database BRIGHTLOOP
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    address VARCHAR(255),
    created_at DATE
);


-- 2. STAFF TABLE

CREATE TABLE IF NOT EXISTS Staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    staff_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'Staff') NOT NULL
);


-- 3. PRODUCTS TABLE

CREATE TABLE IF NOT EXISTS Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    product_type VARCHAR(50),
    sales_price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2),
    notes TEXT
);


-- 4. PRODUCT VARIANTS TABLE

CREATE TABLE IF NOT EXISTS Product_Variants (
    variant_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    variant_name VARCHAR(100),
    additional_price DECIMAL(10,2) DEFAULT 0,

    FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
);


-- 5. SUBSCRIPTION PLANS TABLE

CREATE TABLE IF NOT EXISTS Plans (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_name VARCHAR(100) NOT NULL,
    billing_cycle ENUM('Daily', 'Weekly', 'Monthly', 'Yearly'),
    price DECIMAL(10,2) NOT NULL,
    min_quantity INT DEFAULT 1,
    start_date DATE,
    end_date DATE,
    auto_close BOOLEAN DEFAULT FALSE,
    allow_pause BOOLEAN DEFAULT TRUE,
    allow_renewal BOOLEAN DEFAULT TRUE
);


-- 6. PLAN PRODUCTS TABLE

CREATE TABLE IF NOT EXISTS Plan_Products (
    plan_product_id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,

    FOREIGN KEY (plan_id)
    REFERENCES Plans(plan_id),

    FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
);


-- 7. TAXES TABLE

CREATE TABLE IF NOT EXISTS Taxes (
    tax_id INT AUTO_INCREMENT PRIMARY KEY,
    tax_name VARCHAR(50) NOT NULL,
    tax_percentage DECIMAL(5,2) NOT NULL
);


-- 8. QUOTATION TEMPLATES TABLE

CREATE TABLE IF NOT EXISTS Quotation_Templates (
    template_id INT AUTO_INCREMENT PRIMARY KEY,
    template_name VARCHAR(100) NOT NULL,
    validity_days INT NOT NULL,
    created_date DATE
);


-- 9. QUOTATION TEMPLATE LINES TABLE

CREATE TABLE IF NOT EXISTS Quotation_Template_Lines (
    line_id INT AUTO_INCREMENT PRIMARY KEY,
    template_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10,2),

    FOREIGN KEY (template_id)
    REFERENCES Quotation_Templates(template_id),

    FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
);


-- 10. SUBSCRIPTIONS TABLE

CREATE TABLE IF NOT EXISTS Subscriptions (
    subscription_id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_number VARCHAR(50) UNIQUE NOT NULL,
    customer_id INT NOT NULL,
    plan_id INT NOT NULL,
    start_date DATE,
    expiry_date DATE,
    payment_terms VARCHAR(100),

    status ENUM(
        'Draft',
        'Quotation',
        'Confirmed',
        'Active',
        'Paused',
        'Closed'
    ) DEFAULT 'Draft',

    FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id),

    FOREIGN KEY (plan_id)
    REFERENCES Plans(plan_id)
);


-- 11. SUBSCRIPTION LINES TABLE

CREATE TABLE IF NOT EXISTS Subscription_Lines (
    line_id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    unit_price DECIMAL(10,2),
    tax_id INT,
    amount DECIMAL(10,2),

    FOREIGN KEY (subscription_id)
    REFERENCES Subscriptions(subscription_id),

    FOREIGN KEY (product_id)
    REFERENCES Products(product_id),

    FOREIGN KEY (tax_id)
    REFERENCES Taxes(tax_id)
);


-- 12. DISCOUNTS TABLE

CREATE TABLE IF NOT EXISTS Discounts (
    discount_id INT AUTO_INCREMENT PRIMARY KEY,
    discount_name VARCHAR(100),
    discount_type ENUM('Fixed', 'Percentage'),
    discount_value DECIMAL(10,2),
    minimum_purchase DECIMAL(10,2) DEFAULT 0,
    minimum_quantity INT DEFAULT 1,
    start_date DATE,
    end_date DATE,
    usage_limit INT,
    times_used INT DEFAULT 0
);


-- 13. DISCOUNT PRODUCTS TABLE

CREATE TABLE IF NOT EXISTS Discount_Products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discount_id INT NOT NULL,
    product_id INT NOT NULL,

    FOREIGN KEY (discount_id)
    REFERENCES Discounts(discount_id),

    FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
);


-- 14. SUBSCRIPTION DISCOUNTS TABLE

CREATE TABLE IF NOT EXISTS Subscription_Discounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subscription_id INT NOT NULL,
    discount_id INT NOT NULL,

    FOREIGN KEY (subscription_id)
    REFERENCES Subscriptions(subscription_id),

    FOREIGN KEY (discount_id)
    REFERENCES Discounts(discount_id)
);


-- 15. INVOICES TABLE

CREATE TABLE IF NOT EXISTS Invoices (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_number VARCHAR(50) UNIQUE NOT NULL,
    subscription_id INT NOT NULL,
    customer_id INT NOT NULL,
    invoice_date DATE,
    due_date DATE,
    subtotal DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    discount_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2),

    status ENUM(
        'Draft',
        'Confirmed',
        'Paid',
        'Cancelled'
    ) DEFAULT 'Draft',

    FOREIGN KEY (subscription_id)
    REFERENCES Subscriptions(subscription_id),

    FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
);


-- 16. INVOICE LINES TABLE

CREATE TABLE IF NOT EXISTS Invoice_Lines (
    line_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT,
    unit_price DECIMAL(10,2),
    tax_amount DECIMAL(10,2),
    line_total DECIMAL(10,2),

    FOREIGN KEY (invoice_id)
    REFERENCES Invoices(invoice_id),

    FOREIGN KEY (product_id)
    REFERENCES Products(product_id)
);


-- 17. PAYMENTS TABLE

CREATE TABLE IF NOT EXISTS Payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_id INT NOT NULL,

    payment_method ENUM(
        'Cash',
        'UPI',
        'Card',
        'Bank Transfer'
    ),

    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE,
    notes TEXT,

    FOREIGN KEY (invoice_id)
    REFERENCES Invoices(invoice_id)
);
