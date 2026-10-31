from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/subscriptions",
    tags=["Subscriptions"]
)


@router.get("/{customer_id}")
def get_customer_subscriptions(customer_id: int):

    # TODO: Call the SQL function provided
    # by your database teammate here.

    return {
        "message": "Subscription request received",
        "customer_id": customer_id
    }
