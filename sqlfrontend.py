import mysql.connector
import mysql.connector
import uuid
from decimal import Decimal
from datetime import date, timedelta

def get_connection():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mimi",
        database="Bright loop"
    )

from database.connection import get_connection


# 1. ADD CUSTOMER

def add_customer(name, email, password_hash, phone, address):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Customers
        (customer_name, email, password, phone, address, created_at)
        VALUES (%s, %s, %s, %s, %s, CURDATE())
        """

        values = (name, email, password_hash, phone, address)

        cursor.execute(query, values)
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. DISPLAY ALL CUSTOMERS

def get_all_customers():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT customer_id, customer_name,
                   email, phone, address, created_at
            FROM Customers
        """)

        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 3. SEARCH CUSTOMER BY ID

def get_customer_by_id(customer_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT customer_id, customer_name,
               email, phone, address, created_at
        FROM Customers
        WHERE customer_id = %s
        """

        cursor.execute(query, (customer_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        db.close()


# 4. UPDATE CUSTOMER

def update_customer(customer_id, name, email, phone, address):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Customers
        SET customer_name = %s,
            email = %s,
            phone = %s,
            address = %s
        WHERE customer_id = %s
        """

        values = (name, email, phone, address, customer_id)

        cursor.execute(query, values)
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 5. DELETE CUSTOMER

def delete_customer(customer_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM Customers WHERE customer_id = %s",
            (customer_id,)
        )

        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()



# 1. ADD PRODUCT (Admin/Staff)
def add_product(name, product_type, sales_price, cost_price, notes):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Products
        (product_name, product_type, sales_price, cost_price, notes)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (name, product_type, sales_price, cost_price, notes)

        cursor.execute(query, values)
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. VIEW ALL PRODUCTS (Customer/Admin/Staff)
def get_all_products():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = "SELECT * FROM Products"

        cursor.execute(query)

        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 3. VIEW A PARTICULAR PRODUCT
def get_product_by_id(product_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT * FROM Products
        WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))

        return cursor.fetchone()

    finally:
        cursor.close()
        db.close()


# 4. UPDATE PRODUCT (Admin/Staff)
def update_product(product_id, name, product_type,
                   sales_price, cost_price, notes):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Products
        SET product_name = %s,
            product_type = %s,
            sales_price = %s,
            cost_price = %s,
            notes = %s
        WHERE product_id = %s
        """

        values = (
            name,
            product_type,
            sales_price,
            cost_price,
            notes,
            product_id
        )

        cursor.execute(query, values)
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 5. DELETE PRODUCT (Admin/Staff)
def delete_product(product_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        DELETE FROM Products
        WHERE product_id = %s
        """

        cursor.execute(query, (product_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()



# 1. ADD A PLAN (Admin/Staff)
def add_plan(name, billing_cycle, price, min_quantity,
             start_date, end_date, auto_close,
             allow_pause, allow_renewal):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Plans
        (plan_name, billing_cycle, price, min_quantity,
         start_date, end_date, auto_close,
         allow_pause, allow_renewal)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            name, billing_cycle, price, min_quantity,
            start_date, end_date, auto_close,
            allow_pause, allow_renewal
        )

        cursor.execute(query, values)
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. VIEW AVAILABLE PLANS (Customers/Admin/Staff)
def get_all_plans():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT * FROM Plans
        WHERE (start_date IS NULL OR start_date <= CURDATE())
        AND (end_date IS NULL OR end_date >= CURDATE())
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 3. VIEW ONE PLAN
def get_plan_by_id(plan_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM Plans WHERE plan_id = %s",
            (plan_id,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        db.close()


# 4. VIEW PRODUCTS INCLUDED IN A PLAN
def get_plan_products(plan_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT P.product_id, P.product_name,
               P.sales_price, PP.quantity
        FROM Plan_Products PP
        JOIN Products P ON PP.product_id = P.product_id
        WHERE PP.plan_id = %s
        """

        cursor.execute(query, (plan_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 5. ADD A PRODUCT TO A PLAN (Admin/Staff)
def add_product_to_plan(plan_id, product_id, quantity):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Plan_Products
        (plan_id, product_id, quantity)
        VALUES (%s, %s, %s)
        """

        cursor.execute(query, (plan_id, product_id, quantity))
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 6. UPDATE A PLAN (Admin/Staff)
def update_plan(plan_id, name, billing_cycle, price,
                min_quantity, start_date, end_date,
                auto_close, allow_pause, allow_renewal):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Plans
        SET plan_name = %s,
            billing_cycle = %s,
            price = %s,
            min_quantity = %s,
            start_date = %s,
            end_date = %s,
            auto_close = %s,
            allow_pause = %s,
            allow_renewal = %s
        WHERE plan_id = %s
        """

        values = (
            name, billing_cycle, price, min_quantity,
            start_date, end_date, auto_close,
            allow_pause, allow_renewal, plan_id
        )

        cursor.execute(query, values)
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

# ==========================================
# SUBSCRIPTIONS
# ==========================================

# 1. CREATE A SUBSCRIPTION
def create_subscription(customer_id, plan_id,
                        start_date, expiry_date, payment_terms):

    db = get_connection()
    cursor = db.cursor()

    try:
        # Check that the selected plan exists and is available
        cursor.execute("""
            SELECT * FROM Plans
            WHERE plan_id = %s
            AND (start_date IS NULL OR start_date <= %s)
            AND (end_date IS NULL OR end_date >= %s)
        """, (plan_id, start_date, start_date))

        plan = cursor.fetchone()

        if plan is None:
            raise ValueError("Plan is unavailable.")

        # Generate unique subscription number
        subscription_number = "SUB-" + uuid.uuid4().hex[:10].upper()

        query = """
        INSERT INTO Subscriptions
        (subscription_number, customer_id, plan_id,
         start_date, expiry_date, payment_terms, status)
        VALUES (%s, %s, %s, %s, %s, %s, 'Draft')
        """

        values = (
            subscription_number, customer_id, plan_id,
            start_date, expiry_date, payment_terms
        )

        cursor.execute(query, values)
        db.commit()

        return {
            "subscription_id": cursor.lastrowid,
            "subscription_number": subscription_number
        }

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. ADD A PRODUCT LINE TO A SUBSCRIPTION
def add_subscription_line(subscription_id, product_id,
                          quantity, unit_price, tax_id=None):

    db = get_connection()
    cursor = db.cursor()

    try:
        amount = Decimal(str(quantity)) * Decimal(str(unit_price))

        query = """
        INSERT INTO Subscription_Lines
        (subscription_id, product_id, quantity,
         unit_price, tax_id, amount)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            subscription_id, product_id, quantity,
            unit_price, tax_id, amount
        )

        cursor.execute(query, values)
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 3. VIEW ALL SUBSCRIPTIONS (Admin/Staff)
def get_all_subscriptions():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT S.*, C.customer_name, P.plan_name
        FROM Subscriptions S
        JOIN Customers C ON S.customer_id = C.customer_id
        JOIN Plans P ON S.plan_id = P.plan_id
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 4. VIEW A CUSTOMER'S SUBSCRIPTIONS
def get_customer_subscriptions(customer_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT S.*, P.plan_name, P.price, P.billing_cycle
        FROM Subscriptions S
        JOIN Plans P ON S.plan_id = P.plan_id
        WHERE S.customer_id = %s
        """

        cursor.execute(query, (customer_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 5. VIEW SUBSCRIPTION DETAILS
def get_subscription_by_id(subscription_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT S.*, P.plan_name, P.price, P.billing_cycle,
               C.customer_name, C.email
        FROM Subscriptions S
        JOIN Plans P ON S.plan_id = P.plan_id
        JOIN Customers C ON S.customer_id = C.customer_id
        WHERE S.subscription_id = %s
        """

        cursor.execute(query, (subscription_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        db.close()


# 6. VIEW SUBSCRIPTION PRODUCT LINES
def get_subscription_lines(subscription_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT SL.*, P.product_name, T.tax_name,
               T.tax_percentage
        FROM Subscription_Lines SL
        JOIN Products P ON SL.product_id = P.product_id
        LEFT JOIN Taxes T ON SL.tax_id = T.tax_id
        WHERE SL.subscription_id = %s
        """

        cursor.execute(query, (subscription_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 7. CONFIRM SUBSCRIPTION
def confirm_subscription(subscription_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Subscriptions
        SET status = 'Confirmed'
        WHERE subscription_id = %s
        AND status IN ('Draft', 'Quotation')
        """

        cursor.execute(query, (subscription_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 8. ACTIVATE SUBSCRIPTION
def activate_subscription(subscription_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Subscriptions
        SET status = 'Active'
        WHERE subscription_id = %s
        AND status = 'Confirmed'
        """

        cursor.execute(query, (subscription_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 9. PAUSE SUBSCRIPTION
def pause_subscription(subscription_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Subscriptions S
        JOIN Plans P ON S.plan_id = P.plan_id
        SET S.status = 'Paused'
        WHERE S.subscription_id = %s
        AND S.status = 'Active'
        AND P.allow_pause = TRUE
        """

        cursor.execute(query, (subscription_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 10. RESUME SUBSCRIPTION
def resume_subscription(subscription_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Subscriptions
        SET status = 'Active'
        WHERE subscription_id = %s
        AND status = 'Paused'
        """

        cursor.execute(query, (subscription_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 11. RENEW SUBSCRIPTION
def renew_subscription(subscription_id, new_expiry_date):

    db = get_connection()
    cursor = db.cursor()

    try:
        cursor.execute("""
            UPDATE Subscriptions S
            JOIN Plans P ON S.plan_id = P.plan_id
            SET S.expiry_date = %s,
                S.status = 'Active'
            WHERE S.subscription_id = %s
            AND S.status IN ('Active', 'Closed')
            AND P.allow_renewal = TRUE
        """, (new_expiry_date, subscription_id))

        db.commit()
        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 12. CLOSE SUBSCRIPTION
def close_subscription(subscription_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Subscriptions
        SET status = 'Closed'
        WHERE subscription_id = %s
        AND status IN ('Active', 'Paused', 'Confirmed')
        """

        cursor.execute(query, (subscription_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


from decimal import Decimal, ROUND_HALF_UP
import uuid


# ==========================================
# TAX MANAGEMENT
# ==========================================

# 1. ADD TAX (Admin/Staff)
def add_tax(tax_name, tax_percentage):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Taxes (tax_name, tax_percentage)
        VALUES (%s, %s)
        """

        cursor.execute(query, (tax_name, tax_percentage))
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. VIEW ALL TAXES
def get_all_taxes():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Taxes")
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 3. VIEW ONE TAX
def get_tax_by_id(tax_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM Taxes WHERE tax_id = %s",
            (tax_id,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
        db.close()


# 4. UPDATE TAX
def update_tax(tax_id, tax_name, tax_percentage):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Taxes
        SET tax_name = %s,
            tax_percentage = %s
        WHERE tax_id = %s
        """

        cursor.execute(
            query, (tax_name, tax_percentage, tax_id)
        )

        db.commit()
        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 5. DELETE TAX
def delete_tax(tax_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        cursor.execute(
            "DELETE FROM Taxes WHERE tax_id = %s",
            (tax_id,)
        )

        db.commit()
        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()

# 1. CREATE AN INVOICE FROM A SUBSCRIPTION
def create_invoice(subscription_id, invoice_date, due_date):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Check subscription
        cursor.execute("""
            SELECT *
            FROM Subscriptions
            WHERE subscription_id = %s
            AND status = 'Active'
        """, (subscription_id,))

        subscription = cursor.fetchone()

        if subscription is None:
            raise ValueError("Active subscription not found.")

        # Check whether an invoice already exists
        cursor.execute("""
            SELECT invoice_id
            FROM Invoices
            WHERE subscription_id = %s
            AND invoice_date = %s
        """, (subscription_id, invoice_date))

        if cursor.fetchone():
            raise ValueError("Invoice already exists for this date.")

        # Retrieve subscription products and taxes
        cursor.execute("""
            SELECT SL.product_id,
                   SL.quantity,
                   SL.unit_price,
                   T.tax_percentage
            FROM Subscription_Lines SL
            LEFT JOIN Taxes T
            ON SL.tax_id = T.tax_id
            WHERE SL.subscription_id = %s
        """, (subscription_id,))

        lines = cursor.fetchall()

        if not lines:
            raise ValueError("No products found in subscription.")

        subtotal = Decimal("0.00")
        total_tax = Decimal("0.00")

        invoice_lines = []

        # Calculate product prices and taxes
        for line in lines:

            quantity = Decimal(str(line["quantity"]))
            price = Decimal(str(line["unit_price"]))

            base_amount = (quantity * price).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            tax_rate = Decimal(
                str(line["tax_percentage"] or 0)
            )

            tax_amount = (
                base_amount * tax_rate / Decimal("100")
            ).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )

            line_total = base_amount + tax_amount

            subtotal += base_amount
            total_tax += tax_amount

            invoice_lines.append({
                "product_id": line["product_id"],
                "quantity": line["quantity"],
                "unit_price": price,
                "tax_amount": tax_amount,
                "line_total": line_total
            })

        # Discount will be connected to the Discounts module
        discount_amount = Decimal("0.00")

        total_amount = subtotal + total_tax - discount_amount

        # Generate unique invoice number
        invoice_number = "INV-" + uuid.uuid4().hex[:10].upper()

        # Insert invoice
        cursor.execute("""
            INSERT INTO Invoices
            (invoice_number, subscription_id, customer_id,
             invoice_date, due_date, subtotal, tax_amount,
             discount_amount, total_amount, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'Draft')
        """, (
            invoice_number,
            subscription_id,
            subscription["customer_id"],
            invoice_date,
            due_date,
            subtotal,
            total_tax,
            discount_amount,
            total_amount
        ))

        invoice_id = cursor.lastrowid

        # Insert invoice product lines
        for line in invoice_lines:

            cursor.execute("""
                INSERT INTO Invoice_Lines
                (invoice_id, product_id, quantity,
                 unit_price, tax_amount, line_total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                invoice_id,
                line["product_id"],
                line["quantity"],
                line["unit_price"],
                line["tax_amount"],
                line["line_total"]
            ))

        db.commit()

        return {
            "invoice_id": invoice_id,
            "invoice_number": invoice_number,
            "subtotal": subtotal,
            "tax_amount": total_tax,
            "discount_amount": discount_amount,
            "total_amount": total_amount
        }

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. VIEW ALL INVOICES (Admin/Staff)
def get_all_invoices():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT I.*, C.customer_name, C.email
        FROM Invoices I
        JOIN Customers C
        ON I.customer_id = C.customer_id
        ORDER BY I.invoice_date DESC
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 3. VIEW A CUSTOMER'S INVOICES
def get_customer_invoices(customer_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT *
        FROM Invoices
        WHERE customer_id = %s
        ORDER BY invoice_date DESC
        """

        cursor.execute(query, (customer_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 4. VIEW ONE INVOICE
def get_invoice_by_id(invoice_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT I.*, C.customer_name, C.email,
               C.phone, C.address
        FROM Invoices I
        JOIN Customers C
        ON I.customer_id = C.customer_id
        WHERE I.invoice_id = %s
        """

        cursor.execute(query, (invoice_id,))
        return cursor.fetchone()

    finally:
        cursor.close()
        db.close()


# 5. VIEW PRODUCTS IN AN INVOICE
def get_invoice_lines(invoice_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT IL.*, P.product_name
        FROM Invoice_Lines IL
        JOIN Products P
        ON IL.product_id = P.product_id
        WHERE IL.invoice_id = %s
        """

        cursor.execute(query, (invoice_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 6. CONFIRM AN INVOICE
def confirm_invoice(invoice_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Invoices
        SET status = 'Confirmed'
        WHERE invoice_id = %s
        AND status = 'Draft'
        """

        cursor.execute(query, (invoice_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 7. CANCEL AN INVOICE
def cancel_invoice(invoice_id):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        UPDATE Invoices
        SET status = 'Cancelled'
        WHERE invoice_id = %s
        AND status IN ('Draft', 'Confirmed')
        """

        cursor.execute(query, (invoice_id,))
        db.commit()

        return cursor.rowcount

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 8. VIEW OVERDUE INVOICES
def get_overdue_invoices():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT I.*, C.customer_name, C.email
        FROM Invoices I
        JOIN Customers C
        ON I.customer_id = C.customer_id
        WHERE I.due_date < CURDATE()
        AND I.status = 'Confirmed'
        ORDER BY I.due_date ASC
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# ==========================================
# QUOTATION TEMPLATES AND QUOTATIONS
# ==========================================

# 1. CREATE QUOTATION TEMPLATE (Admin/Staff)
def create_quotation_template(template_name, validity_days):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Quotation_Templates
        (template_name, validity_days, created_date)
        VALUES (%s, %s, CURDATE())
        """

        cursor.execute(query, (template_name, validity_days))
        db.commit()

        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 2. ADD PRODUCT TO QUOTATION TEMPLATE
def add_quotation_template_line(template_id, product_id,
                                quantity, unit_price):

    db = get_connection()
    cursor = db.cursor()

    try:
        query = """
        INSERT INTO Quotation_Template_Lines
        (template_id, product_id, quantity, unit_price)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query, (template_id, product_id, quantity, unit_price)
        )

        db.commit()
        return cursor.lastrowid

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 3. VIEW ALL QUOTATION TEMPLATES
def get_all_quotation_templates():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM Quotation_Templates")
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 4. VIEW PRODUCTS IN A QUOTATION TEMPLATE
def get_quotation_template_lines(template_id):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT QL.*, P.product_name
        FROM Quotation_Template_Lines QL
        JOIN Products P ON QL.product_id = P.product_id
        WHERE QL.template_id = %s
        """

        cursor.execute(query, (template_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()


# 5. CREATE QUOTATION FROM A TEMPLATE
def create_quotation_from_template(customer_id, plan_id,
                                   template_id, start_date,
                                   expiry_date, payment_terms):

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        # Check that the template exists
        cursor.execute("""
            SELECT * FROM Quotation_Templates
            WHERE template_id = %s
        """, (template_id,))

        template = cursor.fetchone()

        if template is None:
            raise ValueError("Quotation template not found.")

        # Get the template's product lines
        cursor.execute("""
            SELECT * FROM Quotation_Template_Lines
            WHERE template_id = %s
        """, (template_id,))

        lines = cursor.fetchall()

        if not lines:
            raise ValueError("Quotation template has no products.")

        # Create subscription with Quotation status
        subscription_number = "SUB-" + uuid.uuid4().hex[:10].upper()

        cursor.execute("""
            INSERT INTO Subscriptions
            (subscription_number, customer_id, plan_id,
             start_date, expiry_date, payment_terms, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Quotation')
        """, (
            subscription_number, customer_id, plan_id,
            start_date, expiry_date, payment_terms
        ))

        subscription_id = cursor.lastrowid

        # Copy template lines into subscription lines
        for line in lines:
            amount = (
                Decimal(str(line["quantity"])) *
                Decimal(str(line["unit_price"]))
            )

            cursor.execute("""
                INSERT INTO Subscription_Lines
                (subscription_id, product_id, quantity,
                 unit_price, tax_id, amount)
                VALUES (%s, %s, %s, %s, NULL, %s)
            """, (
                subscription_id,
                line["product_id"],
                line["quantity"],
                line["unit_price"],
                amount
            ))

        db.commit()

        valid_until = (
            date.today() +
            timedelta(days=template["validity_days"])
        )

        return {
            "subscription_id": subscription_id,
            "subscription_number": subscription_number,
            "status": "Quotation",
            "valid_until": valid_until
        }

    except Exception:
        db.rollback()
        raise

    finally:
        cursor.close()
        db.close()


# 6. VIEW ALL QUOTATIONS
def get_all_quotations():

    db = get_connection()
    cursor = db.cursor(dictionary=True)

    try:
        query = """
        SELECT S.*, C.customer_name, P.plan_name
        FROM Subscriptions S
        JOIN Customers C ON S.customer_id = C.customer_id
        JOIN Plans P ON S.plan_id = P.plan_id
        WHERE S.status = 'Quotation'
        """

        cursor.execute(query)
        return cursor.fetchall()

    finally:
        cursor.close()
        db.close()

