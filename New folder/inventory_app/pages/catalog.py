"""Protected user catalog and checkout route."""

from __future__ import annotations

import reflex as rx

from ..components.cart_section import cart_section
from ..components.product_card import product_card
from ..components.user_navbar import user_navbar
from ..state import AuthState, CartState, InventoryState


@rx.page(route="/catalog", title="KonektPC | Catalog", on_load=AuthState.require_user)
def catalog_page() -> rx.Component:
    """Render the catalog, cart, and order summary."""

    hero = rx.box(
        rx.hstack(
            rx.box(
                rx.icon("shopping_cart", size=30, color="#1D56D8", stroke_width=2),
                width="58px",
                height="58px",
                border_radius="16px",
                background="#FFFFFF",
                border="1px solid #DBEAFE",
                box_shadow="0 10px 24px rgba(29,86,216,.10)",
                display="flex",
                align="center",
                justify="center",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text("Welcome to the Catalog & Checkout", font_size="24px", font_weight="800", color="#132B55", letter_spacing="-0.04em", line_height="1.2"),
                rx.text("Browse available products, add items to your cart, and place an order.", font_size="12px", color="#64748B", margin_top="7px"),
                spacing="0",
                align="start",
            ),
            spacing="4",
            align="center",
            width="100%",
        ),
        class_name="inv-hero",
        width="100%",
        border_radius="16px",
        padding="24px 28px",
        margin_bottom="26px",
    )

    product_grid = rx.cond(
        InventoryState.active_products.length() > 0,
        rx.box(
            rx.foreach(InventoryState.active_products, product_card),
            class_name="inv-product-grid",
            width="100%",
        ),
        rx.box(
            rx.icon("package", size=38, color="#94A3B8"),
            rx.text("No products are currently available", margin_top="8px", font_size="12px", font_weight="700", color="#64748B"),
            width="100%",
            height="260px",
            border="1px dashed #CBD5E1",
            border_radius="16px",
            background="#FFFFFF",
            display="flex",
            flex_direction="column",
            align_items="center",
            justify_content="center",
        ),
    )

    return rx.fragment(
        rx.moment(interval=3000, format="x", on_change=InventoryState.poll),
        rx.moment(interval=3000, format="x", on_change=CartState.poll),
        user_navbar(),
        rx.box(
            rx.vstack(
                hero,
                rx.vstack(
                    rx.hstack(
                        rx.vstack(
                            rx.text("Available Products", font_size="20px", font_weight="800", color="#0F172A", letter_spacing="-0.03em"),
                            rx.text("Select from our current inventory. All items are in stock and ready to order.", font_size="11px", color="#64748B", margin_top="4px"),
                            spacing="0",
                            align="start",
                        ),
                        rx.spacer(),
                        rx.el.span(
                            f"{InventoryState.active_products.length()} Products",
                            background="#DBEAFE",
                            color="#1D4ED8",
                            border_radius="999px",
                            padding="5px 9px",
                            font_size="9px",
                            font_weight="800",
                        ),
                        width="100%",
                        align="center",
                        margin_bottom="14px",
                    ),
                    product_grid,
                    spacing="0",
                    width="100%",
                ),
                cart_section(),
                spacing="0",
                width="100%",
            ),
            class_name="inv-page-inner",
        ),
    )
