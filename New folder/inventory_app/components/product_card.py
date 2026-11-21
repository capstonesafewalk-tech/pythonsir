"""Five-column catalog product card."""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import CartState


def product_card(product: dict[str, Any]) -> rx.Component:
    """Render one available catalog product."""

    out_of_stock = product["stock"] == 0

    return rx.box(
        rx.box(
            rx.el.span(
                product["status"],
                position="absolute",
                top="12px",
                right="12px",
                z_index="2",
                background=product["status_bg"],
                color=product["status_color"],
                border_radius="999px",
                padding="5px 8px",
                font_size="8px",
                font_weight="800",
                box_shadow="0 2px 8px rgba(15,23,42,.04)",
            ),
            rx.image(
                src=product["image"],
                alt=product["name"],
                width="100%",
                height="145px",
                object_fit="cover",
                border_radius="11px",
            ),
            width="100%",
            height="145px",
            position="relative",
            background="#F8FAFC",
            border_radius="11px",
            overflow="hidden",
        ),
        rx.text(
            product["name"],
            margin_top="12px",
            font_size="14px",
            font_weight="800",
            color="#0F172A",
            letter_spacing="-0.02em",
            line_height="1.25",
        ),
        rx.vstack(
            rx.hstack(
                rx.text("Category:", font_size="9px", color="#94A3B8", font_weight="600"),
                rx.text(product["category"], font_size="9px", color="#64748B", font_weight="700"),
                spacing="1",
            ),
            rx.hstack(
                rx.text("SKU:", font_size="9px", color="#94A3B8", font_weight="600"),
                rx.text(product["sku"], font_size="9px", color="#64748B", font_weight="700"),
                spacing="1",
            ),
            spacing="1",
            align="start",
            margin_top="7px",
        ),
        rx.hstack(
            rx.text(product["price_display"], font_size="17px", font_weight="800", color="#0F172A", letter_spacing="-0.03em"),
            rx.spacer(),
            rx.el.span(
                f"Stock: {product['stock']}",
                background=rx.cond(product["stock"] == 0, "#FEE2E2", "#DCFCE7"),
                color=rx.cond(product["stock"] == 0, "#DC2626", "#15803D"),
                border_radius="999px",
                padding="4px 7px",
                font_size="8px",
                font_weight="800",
                white_space="nowrap",
            ),
            width="100%",
            align="center",
            margin_top="14px",
        ),
        rx.el.button(
            rx.icon("plus", size=14, stroke_width=2.5),
            "Add to Cart",
            on_click=CartState.add_to_cart(product["id"]),
            disabled=out_of_stock,
            width="100%",
            height="38px",
            border="none",
            border_radius="9px",
            background="#1D56D8",
            color="#FFFFFF",
            display="flex",
            align="center",
            justify="center",
            gap="6px",
            margin_top="12px",
            font_size="11px",
            font_weight="800",
            class_name="inv-primary-btn",
            opacity=rx.cond(out_of_stock, "0.52", "1"),
        ),
        class_name="inv-card inv-product-card",
        padding="12px",
        width="100%",
        min_width="0",
    )
