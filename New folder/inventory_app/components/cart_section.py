"""Cart summary and order summary components."""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import CartState


def _cart_row(item: dict[str, Any]) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.image(
                src=item["image"],
                alt=item["name"],
                width="58px",
                height="58px",
                border_radius="10px",
                object_fit="cover",
                background="#F8FAFC",
                border="1px solid #EDF2F7",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.text(item["name"], font_size="12px", font_weight="800", color="#0F172A"),
                rx.hstack(
                    rx.text(f"{item['sku']} • {item['category']}", font_size="9px", color="#94A3B8", font_weight="600"),
                    rx.el.span(
                        item["stock_label"],
                        background=item["stock_bg"],
                        color=item["stock_color"],
                        border_radius="999px",
                        padding="3px 7px",
                        font_size="8px",
                        font_weight="800",
                        white_space="nowrap",
                        margin_left="5px",
                    ),
                    spacing="0",
                    align="center",
                    flex_wrap="wrap",
                    margin_top="4px",
                ),
                spacing="0",
                align="start",
                min_width="0",
            ),
            spacing="3",
            align="center",
            min_width="0",
        ),
        rx.hstack(
            rx.el.button(
                rx.icon("minus", size=12, stroke_width=2.5),
                on_click=CartState.decrement_quantity(item["product_id"]),
                width="28px",
                height="28px",
                border_radius="7px",
                border="1px solid #E2E8F0",
                background="#FFFFFF",
                color="#475569",
                display="flex",
                align="center",
                justify="center",
                class_name="inv-icon-btn",
            ),
            rx.text(
                item["quantity"],
                width="30px",
                text_align="center",
                font_size="11px",
                font_weight="800",
                color="#0F172A",
            ),
            rx.el.button(
                rx.icon("plus", size=12, stroke_width=2.5),
                on_click=CartState.increment_quantity(item["product_id"]),
                disabled=~item["can_increment"],
                width="28px",
                height="28px",
                border_radius="7px",
                border="1px solid #E2E8F0",
                background="#FFFFFF",
                color="#475569",
                display="flex",
                align="center",
                justify="center",
                class_name="inv-icon-btn",
                opacity=rx.cond(item["can_increment"], "1", "0.45"),
            ),
            spacing="1",
            align="center",
        ),
        rx.vstack(
            rx.text("Subtotal", font_size="8px", color="#94A3B8", font_weight="700"),
            rx.text(item["line_total_display"], font_size="12px", font_weight="800", color="#0F172A"),
            spacing="0",
            align="end",
        ),
        rx.el.button(
            rx.icon("trash_2", size=14, stroke_width=2.2),
            on_click=CartState.remove_item(item["product_id"]),
            width="30px",
            height="30px",
            border_radius="8px",
            border="1px solid #FECACA",
            background="#FFFFFF",
            color="#DC2626",
            display="flex",
            align="center",
            justify="center",
            class_name="inv-icon-btn",
            title="Remove item",
        ),
        class_name="inv-cart-row",
        width="100%",
        padding="11px 0",
        border_bottom="1px solid #F1F5F9",
    )


def cart_section() -> rx.Component:
    """Render cart summary and order summary side by side."""

    empty_cart = rx.el.div(
        rx.icon("shopping_cart", size=34, color="#CBD5E1", stroke_width=1.8),
        rx.text("Your cart is empty", margin_top="8px", font_size="12px", font_weight="700", color="#64748B"),
        rx.text("Add products from the catalog above.", margin_top="3px", font_size="10px", color="#94A3B8"),
        width="100%",
        height="180px",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
    )

    cart_card = rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.text("Cart Summary", font_size="16px", font_weight="800", color="#0F172A", letter_spacing="-0.02em"),
                    rx.el.span(
                        f"({CartState.item_count} Items)",
                        background="#DBEAFE",
                        color="#1D4ED8",
                        border_radius="999px",
                        padding="4px 8px",
                        font_size="9px",
                        font_weight="800",
                        margin_left="7px",
                    ),
                    spacing="0",
                    align="center",
                ),
                rx.spacer(),
                rx.el.button(
                    rx.icon("trash_2", size=12, stroke_width=2.1),
                    "Clear Cart",
                    on_click=CartState.clear_cart,
                    height="30px",
                    border="1px solid #FECACA",
                    border_radius="8px",
                    background="#FFFFFF",
                    color="#DC2626",
                    display="flex",
                    align="center",
                    gap="5px",
                    padding="0 8px",
                    font_size="9px",
                    font_weight="700",
                    class_name="inv-ghost-btn",
                ),
                width="100%",
                align="center",
            ),
            rx.el.div(height="1px", width="100%", background="#F1F5F9", margin="12px 0 2px"),
            rx.cond(
                CartState.has_items,
                rx.vstack(rx.foreach(CartState.items, _cart_row), spacing="0", width="100%"),
                empty_cart,
            ),
            rx.hstack(
                rx.icon("circle_check", size=14, color="#15803D", stroke_width=2.2),
                rx.text("All items are in stock and ready to order.", font_size="10px", font_weight="700", color="#15803D"),
                spacing="2",
                align="center",
                width="100%",
                height="38px",
                border_radius="9px",
                background="#DCFCE7",
                border="1px solid #BBF7D0",
                padding="0 12px",
                margin_top="10px",
            ),
            spacing="0",
            width="100%",
        ),
        id="cart-summary",
        class_name="inv-card inv-scroll-anchor",
        padding="20px",
        width="100%",
    )

    order_card = rx.box(
        rx.vstack(
            rx.text("Order Summary", font_size="16px", font_weight="800", color="#0F172A", letter_spacing="-0.02em"),
            rx.el.div(height="1px", width="100%", background="#F1F5F9", margin="12px 0 8px"),
            rx.hstack(
                rx.text("Items", font_size="10px", color="#64748B", font_weight="600"),
                rx.text(f"({CartState.item_count})", font_size="10px", color="#334155", font_weight="800"),
                class_name="inv-order-summary-row",
                width="100%",
                margin_bottom="10px",
            ),
            rx.hstack(
                rx.text("Subtotal", font_size="10px", color="#64748B", font_weight="600"),
                rx.text(CartState.subtotal_display, font_size="11px", color="#334155", font_weight="800"),
                class_name="inv-order-summary-row",
                width="100%",
                margin_bottom="10px",
            ),
            rx.hstack(
                rx.text("Shipping", font_size="10px", color="#64748B", font_weight="600"),
                rx.text(CartState.shipping_display, font_size="11px", color="#334155", font_weight="800"),
                class_name="inv-order-summary-row",
                width="100%",
                margin_bottom="12px",
            ),
            rx.el.div(height="1px", width="100%", background="#E2E8F0", margin="0 0 12px"),
            rx.hstack(
                rx.text("Total", font_size="14px", color="#0F172A", font_weight="800"),
                rx.text(CartState.total_display, font_size="20px", color="#0F172A", font_weight="800", letter_spacing="-0.03em"),
                class_name="inv-order-summary-row",
                width="100%",
                margin_bottom="14px",
            ),
            rx.el.button(
                rx.icon("credit_card", size=15, stroke_width=2.2),
                "Checkout",
                on_click=CartState.checkout,
                disabled=~CartState.has_items,
                width="100%",
                height="42px",
                border="none",
                border_radius="9px",
                background="#1D56D8",
                color="#FFFFFF",
                display="flex",
                align="center",
                justify="center",
                gap="7px",
                font_size="12px",
                font_weight="800",
                class_name="inv-primary-btn",
                opacity=rx.cond(CartState.has_items, "1", "0.55"),
            ),
            spacing="0",
            width="100%",
        ),
        class_name="inv-card",
        padding="20px",
        width="100%",
    )

    return rx.box(
        cart_card,
        order_card,
        class_name="inv-checkout-grid",
        width="100%",
        margin_top="22px",
    )
