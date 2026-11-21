"""Searchable, filterable inventory table."""

from __future__ import annotations

from typing import Any

import reflex as rx

from ..state import InventoryState


def _filter_pill(label: str, count: int, value: str) -> rx.Component:
    active = InventoryState.status_filter == value
    return rx.el.button(
        f"{label}",
        rx.el.span(
            rx.text(count),
            margin_left="5px",
            background=rx.cond(active, "rgba(255,255,255,.18)", "#EFF6FF"),
            color=rx.cond(active, "#FFFFFF", "#1D56D8"),
            border_radius="999px",
            padding="1px 6px",
            font_size="9px",
            font_weight="800",
        ),
        on_click=InventoryState.set_filter(value),
        class_name=rx.cond(active, "inv-filter-pill inv-filter-pill-active", "inv-filter-pill"),
        border="1px solid #E2E8F0",
        background="#FFFFFF",
        color="#475569",
        border_radius="999px",
        height="31px",
        padding="0 10px",
        font_size="10px",
        font_weight="700",
        white_space="nowrap",
    )


def _status_badge(product: dict[str, Any]) -> rx.Component:
    return rx.el.span(
        product["status"],
        background=product["status_bg"],
        color=product["status_color"],
        border_radius="999px",
        padding="5px 8px",
        font_size="9px",
        font_weight="800",
        white_space="nowrap",
    )


def _product_row(product: dict[str, Any]) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.hstack(
                rx.image(
                    src=product["image"],
                    alt=product["name"],
                    width="42px",
                    height="42px",
                    border_radius="9px",
                    object_fit="cover",
                    background="#F8FAFC",
                    border="1px solid #EDF2F7",
                ),
                rx.text(
                    product["name"],
                    font_size="12px",
                    font_weight="800",
                    color="#0F172A",
                    white_space="nowrap",
                ),
                spacing="3",
                align="center",
            ),
            padding="10px 12px",
            border_bottom="1px solid #F1F5F9",
        ),
        rx.el.td(product["sku"], padding="10px 12px", border_bottom="1px solid #F1F5F9", font_size="11px", color="#475569", font_weight="700"),
        rx.el.td(product["category"], padding="10px 12px", border_bottom="1px solid #F1F5F9", font_size="11px", color="#64748B"),
        rx.el.td(product["price_display"], padding="10px 12px", border_bottom="1px solid #F1F5F9", font_size="11px", color="#0F172A", font_weight="700", white_space="nowrap"),
        rx.el.td(rx.text(product["stock"]), padding="10px 12px", border_bottom="1px solid #F1F5F9", font_size="11px", color="#334155", font_weight="800"),
        rx.el.td(_status_badge(product), padding="10px 12px", border_bottom="1px solid #F1F5F9"),
        rx.el.td(
            rx.hstack(
                rx.el.button(
                    rx.icon("pencil", size=12, stroke_width=2.2),
                    "Edit",
                    on_click=InventoryState.edit_product(product["id"]),
                    height="29px",
                    border_radius="7px",
                    border="1px solid #E2E8F0",
                    background="#FFFFFF",
                    color="#475569",
                    display="flex",
                    align="center",
                    gap="4px",
                    padding="0 7px",
                    font_size="9px",
                    font_weight="700",
                    class_name="inv-ghost-btn",
                ),
                rx.switch(
                    checked=product["is_active"],
                    on_change=InventoryState.toggle_active(product["id"]),
                    color_scheme="blue",
                    size="1",
                ),
                rx.el.button(
                    "+10",
                    on_click=InventoryState.adjust_stock(product["id"], 10),
                    height="29px",
                    min_width="36px",
                    border_radius="7px",
                    border="1px solid #BBF7D0",
                    background="#DCFCE7",
                    color="#15803D",
                    font_size="9px",
                    font_weight="800",
                    class_name="inv-icon-btn",
                ),
                rx.el.button(
                    "-10",
                    on_click=InventoryState.adjust_stock(product["id"], -10),
                    height="29px",
                    min_width="36px",
                    border_radius="7px",
                    border="1px solid #FECACA",
                    background="#FEE2E2",
                    color="#DC2626",
                    font_size="9px",
                    font_weight="800",
                    class_name="inv-icon-btn",
                ),
                rx.el.button(
                    rx.icon("trash_2", size=13, stroke_width=2.2),
                    on_click=InventoryState.delete_product(product["id"]),
                    width="29px",
                    height="29px",
                    border_radius="7px",
                    border="1px solid #FECACA",
                    background="#FFFFFF",
                    color="#DC2626",
                    display="flex",
                    align="center",
                    justify="center",
                    class_name="inv-icon-btn",
                    title="Delete product",
                ),
                spacing="1",
                align="center",
                flex_wrap="nowrap",
            ),
            padding="10px 12px",
            border_bottom="1px solid #F1F5F9",
        ),
        class_name="inv-table-row",
    )


def inventory_table() -> rx.Component:
    """Render the current inventory card."""

    table_header = rx.el.thead(
        rx.el.tr(
            *[
                rx.el.th(
                    heading,
                    padding="12px",
                    text_align="left",
                    font_size="9px",
                    color="#64748B",
                    font_weight="800",
                    text_transform="uppercase",
                    letter_spacing="0.05em",
                    border_bottom="1px solid #E2E8F0",
                    white_space="nowrap",
                )
                for heading in ["Product", "SKU", "Category", "Price", "Stock", "Status", "Actions"]
            ]
        ),
        background="#F8FAFC",
    )

    table = rx.box(
        rx.el.table(
            table_header,
            rx.el.tbody(rx.foreach(InventoryState.filtered_products, _product_row)),
            width="100%",
            border_collapse="collapse",
            min_width="820px",
        ),
        overflow_x="auto",
        width="100%",
    )

    empty = rx.el.div(
        rx.icon("package", size=34, color="#94A3B8"),
        rx.text("No products match this view", margin_top="8px", font_size="12px", font_weight="700", color="#64748B"),
        width="100%",
        height="220px",
        display="flex",
        flex_direction="column",
        align_items="center",
        justify_content="center",
    )

    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.text("Current Inventory", font_size="17px", font_weight="800", color="#0F172A", letter_spacing="-0.02em"),
                    rx.text("View and manage all products in your inventory.", font_size="11px", color="#64748B", margin_top="3px"),
                    spacing="0",
                    align="start",
                ),
                rx.spacer(),
                rx.el.button(
                    rx.icon("plus", size=15, stroke_width=2.5),
                    "Add Product",
                    on_click=InventoryState.start_add,
                    height="38px",
                    border="none",
                    border_radius="9px",
                    background="#1D56D8",
                    color="#FFFFFF",
                    display="flex",
                    align="center",
                    gap="6px",
                    padding="0 13px",
                    font_size="11px",
                    font_weight="700",
                    box_shadow="0 8px 18px rgba(29,86,216,.16)",
                    class_name="inv-primary-btn",
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.box(
                    rx.icon("search", size=15, color="#94A3B8", position="absolute", left="12px", top="12px", stroke_width=2),
                    rx.el.input(
                        value=InventoryState.search_query,
                        on_change=InventoryState.set_search_query,
                        placeholder="Search products by name, SKU, or category...",
                        height="40px",
                        width="100%",
                        border="1px solid #E2E8F0",
                        border_radius="9px",
                        padding="0 12px 0 36px",
                        font_size="11px",
                        color="#0F172A",
                        outline="none",
                        class_name="inv-search-input",
                    ),
                    position="relative",
                    flex="1",
                    min_width="240px",
                ),
                rx.hstack(
                    _filter_pill("All", InventoryState.total_products, "All"),
                    _filter_pill("In Stock", InventoryState.in_stock_count, "In Stock"),
                    _filter_pill("Low Stock", InventoryState.low_stock_count, "Low Stock"),
                    _filter_pill("Over Stock", InventoryState.over_stock_count, "Over Stock"),
                    spacing="2",
                    flex_wrap="nowrap",
                    align="center",
                ),
                width="100%",
                align="center",
                justify="between",
                spacing="3",
                flex_wrap="wrap",
                margin_top="14px",
                margin_bottom="12px",
            ),
            rx.cond(InventoryState.filtered_products.length() > 0, table, empty),
            spacing="0",
            width="100%",
        ),
        id="inventory",
        class_name="inv-card inv-scroll-anchor",
        padding="20px",
        width="100%",
        overflow="hidden",
    )
