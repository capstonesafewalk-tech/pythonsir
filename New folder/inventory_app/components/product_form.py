"""Add / edit product form used on the admin dashboard."""

from __future__ import annotations

import reflex as rx

from ..models import CATEGORIES
from ..state import InventoryState

INPUT_STYLE = {
    "width": "100%",
    "height": "40px",
    "border": "1px solid #E2E8F0",
    "border_radius": "9px",
    "padding": "0 12px",
    "font_size": "12px",
    "font_weight": "500",
    "color": "#0F172A",
    "background": "#FFFFFF",
    "outline": "none",
    "transition": "border-color .15s ease, box-shadow .15s ease",
}

SELECT_STYLE = {
    **INPUT_STYLE,
    "appearance": "none",
    "background_image": (
        "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' "
        "width='12' height='12' viewBox='0 0 24 24' fill='none' stroke='%2364748B' "
        "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E"
        "%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E\")"
    ),
    "background_repeat": "no-repeat",
    "background_position": "right 12px center",
    "padding_right": "32px",
}


def _label(text: str, required: bool = True) -> rx.Component:
    return rx.hstack(
        rx.text(
            text,
            font_size="11px",
            font_weight="700",
            color="#334155",
        ),
        rx.text(
            "*",
            font_size="11px",
            font_weight="800",
            color="#EF4444",
        )
        if required
        else rx.fragment(),
        spacing="1",
        align="center",
    )


def _field(label: str, control: rx.Component, required: bool = True) -> rx.Component:
    return rx.vstack(
        _label(label, required),
        control,
        spacing="2",
        align="start",
        width="100%",
    )


def product_form() -> rx.Component:
    """Render the create/update product card."""

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon("boxes", size=19, color="#1D56D8", stroke_width=2.1),
                    width="38px",
                    height="38px",
                    border_radius="11px",
                    background="#EAF2FF",
                    display="flex",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.hstack(
                        rx.text(
                            InventoryState.form_title,
                            font_size="16px",
                            font_weight="800",
                            color="#0F172A",
                            letter_spacing="-0.02em",
                        ),
                        rx.cond(
                            InventoryState.is_editing,
                            rx.el.span(
                                "EDITING",
                                background="#DBEAFE",
                                color="#1D4ED8",
                                border_radius="999px",
                                padding="3px 7px",
                                font_size="8px",
                                font_weight="800",
                                letter_spacing="0.08em",
                            ),
                            rx.fragment(),
                        ),
                        spacing="2",
                        align="center",
                    ),
                    rx.text(
                        InventoryState.form_subtitle,
                        font_size="11px",
                        color="#64748B",
                        line_height="1.45",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
            ),
            rx.el.div(
                width="100%",
                height="1px",
                background="#F1F5F9",
                margin="16px 0 2px",
            ),
            _field(
                "Product Name",
                rx.el.input(
                    value=InventoryState.form_name,
                    on_change=InventoryState.set_form_name,
                    placeholder="Enter product name",
                    class_name="inv-input",
                    style=INPUT_STYLE,
                ),
            ),
            _field(
                "SKU",
                rx.el.input(
                    value=InventoryState.form_sku,
                    on_change=InventoryState.set_form_sku,
                    placeholder="e.g., KB-001",
                    class_name="inv-input",
                    style=INPUT_STYLE,
                ),
            ),
            _field(
                "Category",
                rx.el.select(
                    *[
                        rx.el.option(category, value=category)
                        for category in CATEGORIES
                    ],
                    value=InventoryState.form_category,
                    on_change=InventoryState.set_form_category,
                    class_name="inv-select",
                    style=SELECT_STYLE,
                ),
            ),
            rx.hstack(
                _field(
                    "Price",
                    rx.el.input(
                        value=InventoryState.form_price,
                        on_change=InventoryState.set_form_price,
                        placeholder="0.00",
                        input_mode="decimal",
                        class_name="inv-input",
                        style=INPUT_STYLE,
                    ),
                ),
                _field(
                    "Stock",
                    rx.el.input(
                        value=InventoryState.form_stock,
                        on_change=InventoryState.set_form_stock,
                        placeholder="0",
                        input_mode="numeric",
                        class_name="inv-input",
                        style=INPUT_STYLE,
                    ),
                ),
                spacing="3",
                width="100%",
                align="start",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Active Product",
                        font_size="11px",
                        font_weight="700",
                        color="#334155",
                    ),
                    rx.text(
                        "Product is visible and available for ordering",
                        font_size="9px",
                        color="#94A3B8",
                        line_height="1.4",
                    ),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.switch(
                    checked=InventoryState.form_active,
                    on_change=InventoryState.set_form_active,
                    color_scheme="blue",
                    size="2",
                ),
                width="100%",
                align="center",
                background="#F8FAFC",
                border="1px solid #EEF2F7",
                border_radius="10px",
                padding="10px 12px",
            ),
            rx.hstack(
                rx.el.button(
                    rx.icon("check", size=15, stroke_width=2.6),
                    InventoryState.save_label,
                    on_click=InventoryState.save_product,
                    display="flex",
                    align="center",
                    justify="center",
                    gap="7px",
                    background="#1D56D8",
                    color="#FFFFFF",
                    border="none",
                    border_radius="9px",
                    padding="0 16px",
                    height="40px",
                    font_size="12px",
                    font_weight="700",
                    box_shadow="0 8px 18px rgba(29, 86, 216, 0.18)",
                    flex="1",
                    class_name="inv-primary-btn",
                ),
                rx.el.button(
                    rx.icon("rotate_ccw", size=14, stroke_width=2.2),
                    "Reset",
                    on_click=InventoryState.reset_form,
                    display="flex",
                    align="center",
                    justify="center",
                    gap="7px",
                    background="#FFFFFF",
                    color="#475569",
                    border="1px solid #E2E8F0",
                    border_radius="9px",
                    padding="0 14px",
                    height="40px",
                    font_size="12px",
                    font_weight="600",
                    class_name="inv-ghost-btn",
                ),
                spacing="2",
                width="100%",
                margin_top="2px",
            ),
            spacing="3",
            width="100%",
            align="start",
        ),
        class_name="inv-card",
        padding="20px",
        width="100%",
    )
