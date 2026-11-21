"""Admin dashboard top header."""

from __future__ import annotations

import reflex as rx

from ..state import AuthState


def _bell_button() -> rx.Component:
    return rx.box(
        rx.icon("bell", size=19, color="#475569", stroke_width=2),
        rx.el.span(
            width="7px",
            height="7px",
            border_radius="999px",
            background="#EF4444",
            border="2px solid #FFFFFF",
            position="absolute",
            top="9px",
            right="10px",
        ),
        position="relative",
        width="42px",
        height="42px",
        border_radius="12px",
        background="#FFFFFF",
        border="1px solid #E2E8F0",
        display="flex",
        align="center",
        justify="center",
        box_shadow="0 1px 2px rgba(15, 23, 42, 0.04)",
        cursor="pointer",
        title="Notifications",
        on_click=rx.toast.info("You have 3 new inventory notifications."),
    )


def admin_header() -> rx.Component:
    """Render the dashboard title and administrator controls."""

    return rx.hstack(
        rx.vstack(
            rx.hstack(
                rx.text(
                    "Admin Dashboard",
                    font_size="28px",
                    font_weight="800",
                    color="#0F172A",
                    letter_spacing="-0.035em",
                    line_height="1.2",
                ),
                rx.el.span(
                    "LIVE",
                    background="#DCFCE7",
                    color="#15803D",
                    border_radius="999px",
                    padding="3px 8px",
                    font_size="9px",
                    font_weight="800",
                    letter_spacing="0.08em",
                    margin_left="10px",
                ),
                align="center",
                spacing="0",
            ),
            rx.text(
                "Manage your inventory, orders, and product catalog",
                color="#64748B",
                font_size="13px",
                font_weight="400",
                margin_top="4px",
            ),
            spacing="0",
            align="start",
        ),
        rx.spacer(),
        rx.hstack(
            _bell_button(),
            rx.hstack(
                rx.box(
                    "A",
                    width="34px",
                    height="34px",
                    border_radius="10px",
                    background="linear-gradient(135deg, #1D56D8, #132B55)",
                    color="#FFFFFF",
                    font_size="13px",
                    font_weight="800",
                    display="flex",
                    align="center",
                    justify="center",
                ),
                rx.vstack(
                    rx.text(
                        "Administrator",
                        color="#0F172A",
                        font_size="12px",
                        font_weight="700",
                        line_height="1.2",
                    ),
                    rx.text(
                        AuthState.auth_user,
                        color="#94A3B8",
                        font_size="10px",
                        line_height="1.2",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="2",
                align="center",
                background="#FFFFFF",
                border="1px solid #E2E8F0",
                border_radius="12px",
                padding="5px 12px 5px 6px",
                box_shadow="0 1px 2px rgba(15, 23, 42, 0.04)",
            ),
            rx.el.button(
                rx.icon("log_out", size=15, stroke_width=2),
                "Logout",
                on_click=AuthState.logout,
                display="flex",
                align="center",
                gap="7px",
                background="#FFFFFF",
                color="#475569",
                border="1px solid #E2E8F0",
                border_radius="10px",
                padding="10px 14px",
                font_size="12px",
                font_weight="600",
                box_shadow="0 1px 2px rgba(15, 23, 42, 0.04)",
                _hover={"background": "#F8FAFC", "border_color": "#CBD5E1"},
                class_name="inv-ghost-btn",
            ),
            spacing="3",
            align="center",
        ),
        width="100%",
        align="center",
        justify="between",
        padding="30px 32px 22px",
    )
