from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/subscriptions",
    tags=["Subscriptions"]
)


@router.get("/{customer_id}")
def get_customer_subscriptions(customer_id: int):

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

    return {
        "message": "Subscription request received",
        "customer_id": customer_id
    }
    from fastapi import APIRouter, HTTPException, Depends

from sqlfrontend import get_all_customers
from auth import get_current_user

router = APIRouter(
    prefix="/api/admin",
    tags=["Admin"]
)


@router.get("/customers")
def display_all_customers(
    current_user=Depends(get_current_user)
):

    # Only Admin can view all customers
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admin only."
        )

    # Calling your friend's SQL function
    customers = get_all_customers()

    return {
        "message": "Customers retrieved successfully",
        "customers": customers
    }
