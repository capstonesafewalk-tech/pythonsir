"""Database models and seed data for the Inventory & Ordering System."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Final

import reflex as rx
from pydantic import BaseModel as PydanticBaseModel, NaiveDatetime
from sqlmodel import Field, Session, select

# Reflex 0.6 exposed ``rx.Base`` while newer releases use Pydantic directly.
# This keeps the helper model compatible with both APIs.
BaseModelBase = getattr(rx, "Base", PydanticBaseModel)

CATEGORIES: Final[list[str]] = ["Accessories", "Electronics", "Office"]
DEFAULT_PRODUCT_IMAGE: Final[str] = "/products/generic.svg"


class CartItem(BaseModelBase):
    """Serializable cart line stored in the browser session state."""

    product_id: int
    name: str
    sku: str
    category: str
    price: float
    stock: int
    quantity: int
    image: str


class Product(rx.Model, table=True):
    """A product available in the inventory and catalog."""

    __tablename__ = "products"

    name: str = Field(index=True)
    sku: str = Field(index=True, unique=True)
    category: str = Field(index=True)
    price: float = Field(default=0.0, ge=0)
    stock: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    image: str = Field(default=DEFAULT_PRODUCT_IMAGE)
    created_at: NaiveDatetime = Field(default_factory=datetime.now)


class Order(rx.Model, table=True):
    """A customer order created at checkout."""

    __tablename__ = "orders"

    order_number: str = Field(index=True, unique=True)
    item_count: int = Field(default=0, ge=0)
    total: float = Field(default=0.0, ge=0)
    status: str = Field(default="Processing")
    created_at: NaiveDatetime = Field(default_factory=datetime.now)


class OrderItem(rx.Model, table=True):
    """A snapshot of a purchased product on an order."""

    __tablename__ = "order_items"

    order_id: int = Field(index=True)
    product_id: int
    product_name: str
    sku: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)
    line_total: float = Field(ge=0)


PRODUCT_SEEDS: Final[list[dict[str, Any]]] = [
    {
        "name": "Keyboard",
        "sku": "KB-001",
        "category": "Accessories",
        "price": 49.99,
        "stock": 18,
        "is_active": True,
        "image": "/products/keyboard.svg",
    },
    {
        "name": "Wireless Mouse",
        "sku": "MS-002",
        "category": "Accessories",
        "price": 29.99,
        "stock": 8,
        "is_active": True,
        "image": "/products/mouse.svg",
    },
    {
        "name": "Monitor",
        "sku": "MN-003",
        "category": "Electronics",
        "price": 199.99,
        "stock": 25,
        "is_active": True,
        "image": "/products/monitor.svg",
    },
    {
        "name": "Laptop Stand",
        "sku": "LS-004",
        "category": "Office",
        "price": 59.99,
        "stock": 55,
        "is_active": True,
        "image": "/products/laptop-stand.svg",
    },
    {
        "name": "USB-C Hub",
        "sku": "UH-005",
        "category": "Accessories",
        "price": 79.99,
        "stock": 12,
        "is_active": True,
        "image": "/products/usb-hub.svg",
    },
]

# (sku, quantity, status, minutes_ago) rows. Order #12 deliberately mirrors the
# two-item, $129.98 order shown in the reference design.
ORDER_SEEDS: Final[list[dict[str, Any]]] = [
    {
        "items": [("MN-003", 1)],
        "status": "Completed",
        "minutes_ago": 4320,
    },
    {
        "items": [("KB-001", 2)],
        "status": "Completed",
        "minutes_ago": 3600,
    },
    {
        "items": [("MS-002", 3)],
        "status": "Completed",
        "minutes_ago": 3120,
    },
    {
        "items": [("LS-004", 1), ("MS-002", 1)],
        "status": "Completed",
        "minutes_ago": 2760,
    },
    {
        "items": [("UH-005", 2)],
        "status": "Completed",
        "minutes_ago": 2280,
    },
    {
        "items": [("MN-003", 1), ("KB-001", 1)],
        "status": "Completed",
        "minutes_ago": 1920,
    },
    {
        "items": [("KB-001", 1), ("MS-002", 1)],
        "status": "Completed",
        "minutes_ago": 1320,
    },
    {
        "items": [("LS-004", 1)],
        "status": "Completed",
        "minutes_ago": 960,
    },
    {
        "items": [("UH-005", 1), ("MS-002", 1)],
        "status": "Completed",
        "minutes_ago": 540,
    },
    {
        "items": [("MN-003", 1)],
        "status": "Completed",
        "minutes_ago": 280,
    },
    {
        "items": [("KB-001", 2), ("LS-004", 1)],
        "status": "Processing",
        "minutes_ago": 105,
    },
    {
        "items": [("KB-001", 1), ("UH-005", 1)],
        "status": "Processing",
        "minutes_ago": 12,
    },
]


def status_for_stock(stock: int) -> tuple[str, str, str]:
    """Return the stock badge label, background, and text color."""

    if stock == 0:
        return "Out of Stock", "#FEE2E2", "#DC2626"
    if 1 <= stock <= 10:
        return "Low Stock", "#FEF3C7", "#B45309"
    if 11 <= stock <= 49:
        return "In Stock", "#DCFCE7", "#15803D"
    return "Over Stock", "#DBEAFE", "#1D4ED8"


def stock_bucket(stock: int) -> str:
    """Return the stock bucket used by inventory filters."""

    if stock == 0:
        return "Out of Stock"
    if 1 <= stock <= 10:
        return "Low Stock"
    if 11 <= stock <= 49:
        return "In Stock"
    return "Over Stock"


def image_for_category(category: str) -> str:
    """Pick a clean fallback render for newly created products."""

    return {
        "Accessories": "/products/usb-hub.svg",
        "Electronics": "/products/monitor.svg",
        "Office": "/products/laptop-stand.svg",
    }.get(category, DEFAULT_PRODUCT_IMAGE)


def format_currency(amount: float) -> str:
    """Format a number as US currency."""

    return f"₱{amount:,.2f}"


def format_time_ago(created_at: datetime) -> str:
    """Format a timestamp as a compact relative label."""

    delta = datetime.now() - created_at
    seconds = max(int(delta.total_seconds()), 0)
    if seconds < 60:
        return "Just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} min ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hr ago"
    days = hours // 24
    if days == 1:
        return "Yesterday"
    return f"{days} days ago"


def product_to_dict(product: Product) -> dict[str, Any]:
    """Serialize a product for the inventory table and catalog cards."""

    status, status_bg, status_color = status_for_stock(product.stock)
    return {
        "id": product.id or 0,
        "name": product.name,
        "sku": product.sku,
        "category": product.category,
        "price": product.price,
        "price_display": format_currency(product.price),
        "stock": product.stock,
        "stock_label": f"Stock: {product.stock}",
        "status": status,
        "status_bg": status_bg,
        "status_color": status_color,
        "is_active": product.is_active,
        "image": product.image or DEFAULT_PRODUCT_IMAGE,
    }


def order_to_dict(order: Order) -> dict[str, Any]:
    """Serialize an order for the recent-orders card."""

    is_completed = order.status == "Completed"
    return {
        "id": order.id or 0,
        "number": f"#ORD-{order.order_number.split('-')[-1]}",
        "order_number": order.order_number,
        "item_count": order.item_count,
        "items_label": f"{order.item_count} item{'s' if order.item_count != 1 else ''}",
        "total": order.total,
        "total_display": format_currency(order.total),
        "status": order.status,
        "status_bg": "#DCFCE7" if is_completed else "#DBEAFE",
        "status_color": "#15803D" if is_completed else "#1D4ED8",
        "time_ago": format_time_ago(order.created_at),
    }


def next_order_number(session: Session) -> str:
    """Return the next sequential order number."""

    orders = session.exec(select(Order)).all()
    highest = 0
    for order in orders:
        try:
            highest = max(highest, int(order.order_number.split("-")[-1]))
        except (ValueError, IndexError):
            continue
    return f"ORD-{highest + 1:04d}"


def _seed_orders(session: Session) -> None:
    """Seed a realistic order history when the order table is empty."""

    products = {
        product.sku: product
        for product in session.exec(select(Product)).all()
    }
    now = datetime.now()
    for index, seed in enumerate(ORDER_SEEDS, start=1):
        items: list[tuple[str, int]] = seed["items"]
        total = 0.0
        item_count = 0
        for sku, quantity in items:
            product = products.get(sku)
            if product is None:
                continue
            total += product.price * quantity
            item_count += quantity

        order = Order(
            order_number=f"ORD-{index:04d}",
            item_count=item_count,
            total=round(total, 2),
            status=seed["status"],
            created_at=now - timedelta(minutes=int(seed["minutes_ago"])),
        )
        session.add(order)
        session.flush()

        for sku, quantity in items:
            product = products.get(sku)
            if product is None:
                continue
            session.add(
                OrderItem(
                    order_id=order.id or 0,
                    product_id=product.id or 0,
                    product_name=product.name,
                    sku=product.sku,
                    quantity=quantity,
                    unit_price=product.price,
                    line_total=round(product.price * quantity, 2),
                )
            )
    session.commit()


def init_db() -> None:
    """Create all tables and seed the database once."""

    rx.model.create_all()
    with rx.session() as session:
        if session.exec(select(Product)).first() is None:
            for product_seed in PRODUCT_SEEDS:
                session.add(Product(**product_seed))
            session.commit()

        if session.exec(select(Order)).first() is None:
            _seed_orders(session)
