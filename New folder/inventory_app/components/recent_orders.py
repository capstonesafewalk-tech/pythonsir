"""Recent customer orders card."""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import OrderState


def _order_row(order: dict[str, Any]) -> rx.Component:
    return rx.el.button(
        rx.hstack(
            rx.box(
                rx.icon("shopping_bag", size=16, color="#1D56D8", stroke_width=2.1),
                width="34px",
                height="34px",
                border_radius="9px",
                background="#EAF2FF",
                display="flex",
                align="center",
                justify="center",
                flex_shrink="0",
            ),
            rx.vstack(
                rx.hstack(
                    rx.text(order["number"], font_size="11px", font_weight="800", color="#0F172A"),
                    rx.el.span("•", color="#CBD5E1", font_size="10px"),
                    rx.text(order["items_label"], font_size="10px", color="#64748B", font_weight="600"),
                    rx.el.span("•", color="#CBD5E1", font_size="10px"),
                    rx.text(order["total_display"], font_size="11px", color="#334155", font_weight="800"),
                    spacing="2",
                    align="center",
                    flex_wrap="wrap",
                ),
                rx.text(order["time_ago"], font_size="9px", color="#94A3B8", margin_top="3px"),
                spacing="0",
                align="start",
            ),
            rx.spacer(),
            rx.el.span(
                order["status"],
                background=order["status_bg"],
                color=order["status_color"],
                border_radius="999px",
                padding="4px 8px",
                font_size="9px",
                font_weight="800",
                white_space="nowrap",
            ),
            width="100%",
            align="center",
            spacing="3",
        ),
        on_click=OrderState.toggle_status(order["id"]),
        class_name="inv-order-row",
        width="100%",
        background="#FFFFFF",
        border="1px solid #EDF2F7",
        border_radius="10px",
        padding="9px",
        text_align="left",
        cursor="pointer",
        title="Click to toggle order status",
    )


def recent_orders() -> rx.Component:
    """Render the latest order list."""

    empty = rx.el.div(
        rx.icon("shopping_cart", size=30, color="#94A3B8"),
        rx.text("No orders yet", margin_top="7px", font_size="11px", color="#64748B", font_weight="700"),
        height="180px",
        width="100%",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
    )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Recent Orders", font_size="16px", font_weight="800", color="#0F172A", letter_spacing="-0.02em"),
                    rx.text("Latest customer orders and status", font_size="10px", color="#64748B", margin_top="3px"),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.el.span(
                    "LIVE",
                    background="#EAF2FF",
                    color="#1D56D8",
                    border_radius="999px",
                    padding="3px 7px",
                    font_size="8px",
                    font_weight="800",
                    letter_spacing="0.08em",
                ),
                width="100%",
                align="center",
            ),
            rx.el.div(height="1px", width="100%", background="#F1F5F9", margin="12px 0 4px"),
            rx.cond(
                OrderState.recent_orders.length() > 0,
                rx.vstack(
                    rx.foreach(OrderState.recent_orders, _order_row),
                    spacing="2",
                    width="100%",
                ),
                empty,
            ),
            spacing="0",
            width="100%",
        ),
        id="orders",
        class_name="inv-card inv-scroll-anchor",
        padding="20px",
        width="100%",
    )
