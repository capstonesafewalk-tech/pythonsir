"""Dark navy user catalog navigation bar."""

from __future__ import annotations

import reflex as rx

from ..state import AuthState, CartState


def user_navbar() -> rx.Component:
    """Render the catalog and checkout top navigation."""

    return rx.box(
        rx.hstack(
            rx.hstack(
                rx.box(
                    rx.image(src="/brand/cube.svg", alt="Inventory", width="38px", height="38px"),
                    width="42px",
                    height="42px",
                    border_radius="12px",
                    background="rgba(96,165,250,.12)",
                    border="1px solid rgba(147,197,253,.16)",
                    display="flex",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.text("KonektPC", color="#FFFFFF", font_size="16px", font_weight="800", letter_spacing="-0.02em", line_height="1.15"),
                    rx.text("Python Reflex", color="#9DB5D8", font_size="10px", font_weight="600", line_height="1.2", margin_top="3px"),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
            ),
            rx.spacer(),
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("circle_user_round", size=16, color="#D7E4F8", stroke_width=2),
                        width="28px",
                        height="28px",
                        border_radius="999px",
                        background="rgba(255,255,255,.09)",
                        display="flex",
                        align="center",
                        justify="center",
                    ),
                    rx.text("User", color="#FFFFFF", font_size="11px", font_weight="700"),
                    spacing="2",
                    align="center",
                    height="38px",
                    border_radius="999px",
                    border="1px solid rgba(255,255,255,.12)",
                    background="rgba(255,255,255,.06)",
                    padding="0 12px 0 5px",
                ),
                rx.el.button(
                    rx.icon("shopping_cart", size=15, color="#0F172A", stroke_width=2.2),
                    CartState.cart_badge,
                    on_click=rx.scroll_to("cart-summary"),
                    height="38px",
                    border="none",
                    border_radius="999px",
                    background="#FFFFFF",
                    color="#0F172A",
                    display="flex",
                    align="center",
                    gap="7px",
                    padding="0 13px",
                    font_size="11px",
                    font_weight="800",
                    class_name="inv-icon-btn",
                ),
                rx.el.button(
                    rx.icon("log_out", size=14, stroke_width=2),
                    "Logout",
                    on_click=AuthState.logout,
                    height="38px",
                    border_radius="9px",
                    border="1px solid rgba(255,255,255,.16)",
                    background="rgba(255,255,255,.08)",
                    color="#FFFFFF",
                    display="flex",
                    align="center",
                    gap="6px",
                    padding="0 12px",
                    font_size="11px",
                    font_weight="700",
                    class_name="inv-icon-btn",
                ),
                spacing="2",
                align="center",
            ),
            width="100%",
            align="center",
            class_name="inv-navbar-inner",
            height="72px",
        ),
        width="100%",
        background="#132B55",
        box_shadow="0 8px 24px rgba(19,43,85,.12)",
        position="sticky",
        top="0",
        z_index="50",
    )
