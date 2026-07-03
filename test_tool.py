from app.tools.support_tools import (
    lookup_order,
    refund_policy,
    shipping_policy,
    create_ticket,
)

print("=" * 40)

print(
    lookup_order.invoke(
        {"order_id": "ORD002"}
    )
)

print("=" * 40)

print(
    refund_policy.invoke({})
)

print("=" * 40)

print(
    shipping_policy.invoke({})
)

print("=" * 40)

print(
    create_ticket.invoke(
        {"issue": "Laptop won't boot"}
    )
)