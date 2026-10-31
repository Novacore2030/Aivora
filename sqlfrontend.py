import mysql.connector

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
