from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr

from sqlfrontend import (
    add_customer,
    get_all_customers,
    delete_customer
)
from auth import get_current_user, hash_password

router = APIRouter(prefix="/api/admin", tags=["Admin"])


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    phone: str
    address: str


# ADD CUSTOMER
@router.post("/customers")
def create_customer(
    customer: CustomerCreate,
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "Admin":
        raise HTTPException(status_code=403, detail="Admin only")

    try:
        customer_id = add_customer(
            customer.name,
            customer.email,
            hash_password(customer.password),
            customer.phone,
            customer.address
        )
        return {
            "message": "Customer added successfully",
            "customer_id": customer_id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# DISPLAY ALL CUSTOMERS
@router.get("/customers")
def display_customers(current_user=Depends(get_current_user)):
    if current_user["role"] != "Admin":
        raise HTTPException(status_code=403, detail="Admin only")

    return {"customers": get_all_customers()}


# DELETE CUSTOMER
@router.delete("/customers/{customer_id}")
def remove_customer(
    customer_id: int,
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "Admin":
        raise HTTPException(status_code=403, detail="Admin only")

    result = delete_customer(customer_id)

    if result == 0:
        raise HTTPException(status_code=404, detail="Customer not found")

    return {"message": "Customer deleted successfully"}
