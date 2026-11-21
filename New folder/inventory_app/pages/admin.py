"""Protected administrator dashboard route."""

from __future__ import annotations

import reflex as rx

from ..components.admin_header import admin_header
from ..components.inventory_table import inventory_table
from ..components.kpi_cards import kpi_cards
from ..components.product_form import product_form
from ..components.recent_orders import recent_orders
from ..components.sidebar import sidebar
from ..state import AuthState, InventoryState, OrderState


@rx.page(route="/admin", title="KonektPC | Admin Dashboard", on_load=AuthState.require_admin)
def admin_page() -> rx.Component:
    """Render the complete admin dashboard."""

    return rx.fragment(
        rx.moment(interval=3000, format="x", on_change=InventoryState.poll),
        rx.moment(interval=3000, format="x", on_change=OrderState.poll),
        sidebar(),
        rx.box(
            admin_header(),
            rx.box(
                kpi_cards(),
                rx.box(
                    rx.vstack(
                        rx.box(product_form(), width="100%"),
                        rx.box(recent_orders(), width="100%"),
                        spacing="4",
                        width="100%",
                        align="start",
                    ),
                    rx.box(inventory_table(), width="100%"),
                    class_name="inv-admin-grid",
                    width="100%",
                    margin_top="22px",
                ),
                class_name="inv-page-inner",
                padding_top="0",
            ),
            class_name="inv-main",
            width="100%",
        ),
    )
