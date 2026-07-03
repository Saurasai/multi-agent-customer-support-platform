from langchain_core.tools import tool


@tool
def lookup_order(order_id: str) -> dict:
    """
    Look up an order using its order ID.

    Returns the order status and estimated delivery date.
    """

    dummy_orders = {
        "ORD001": {
            "status": "Delivered",
            "estimated_delivery": "Delivered",
        },
        "ORD002": {
            "status": "Processing",
            "estimated_delivery": "Tomorrow",
        },
        "ORD003": {
            "status": "Cancelled",
            "estimated_delivery": None,
        },
        "ORD004": {
            "status": "Shipped",
            "estimated_delivery": "2 days",
        },
    }

    order = dummy_orders.get(order_id)

    if order is None:
        return {
            "success": False,
            "error": "Order not found",
        }

    return {
        "success": True,
        "order_id": order_id,
        **order,
    }


@tool
def refund_policy() -> dict:
    """
    Return the company's refund policy.
    """

    return {
        "success": True,
        "refund_window": "30 days",
        "processing_time": "5 business days",
        "digital_products": "Non-refundable",
        "damaged_products": "Not covered if caused by misuse",
    }


@tool
def shipping_policy() -> dict:
    """
    Return the company's shipping policy.
    """

    return {
        "success": True,
        "standard_shipping": "5-7 business days",
        "express_shipping": "1-2 business days",
        "tracking": "Tracking ID is provided after shipment",
    }


@tool
def create_ticket(issue: str) -> dict:
    """
    Create a customer support ticket.
    """

    ticket_id = "TKT1001"

    return {
        "success": True,
        "ticket_id": ticket_id,
        "issue": issue,
        "status": "Created",
    }