"""Computed KPI summary cards for the admin dashboard."""

from __future__ import annotations

import reflex as rx

from ..state import InventoryState, OrderState


def _trend_pill(text: str, background: str, color: str) -> rx.Component:
    return rx.hstack(
        rx.icon("arrow_up_right", size=11, stroke_width=2.6),
        rx.text(text, font_size="10px", font_weight="700"),
        spacing="1",
        align="center",
        background=background,
        color=color,
        border_radius="999px",
        padding="4px 8px",
        width="fit-content",
    )


def _kpi_card(
    *,
    icon: str,
    icon_background: str,
    icon_color: str,
    label: str,
    value: rx.Var[int] | int,
    trend: str,
    trend_background: str,
    trend_color: str,
    accent: str,
) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.icon(icon, size=20, color=icon_color, stroke_width=2.2),
                    width="42px",
                    height="42px",
                    border_radius="12px",
                    background=icon_background,
                    display="flex",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                rx.spacer(),
                _trend_pill(trend, trend_background, trend_color),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.vstack(
                    rx.text(
                        value,
                        font_size="30px",
                        font_weight="800",
                        color="#0F172A",
                        letter_spacing="-0.04em",
                        line_height="1",
                    ),
                    rx.text(
                        label,
                        color="#64748B",
                        font_size="12px",
                        font_weight="600",
                    ),
                    spacing="1",
                    align="start",
                ),
                rx.spacer(),
                rx.el.span(
                    width="4px",
                    height="44px",
                    border_radius="999px",
                    background=accent,
                    opacity="0.8",
                ),
                width="100%",
                align="end",
            ),
            spacing="4",
            width="100%",
            align="start",
        ),
        class_name="inv-card",
        padding="20px",
        min_height="132px",
        position="relative",
        overflow="hidden",
    )


def kpi_cards() -> rx.Component:
    """Render the three live KPI cards."""

    return rx.box(
        _kpi_card(
            icon="package",
            icon_background="#EAF2FF",
            icon_color="#1D56D8",
            label="Total Products",
            value=InventoryState.total_products,
            trend="+2 vs. last week",
            trend_background="#DCFCE7",
            trend_color="#15803D",
            accent="#1D56D8",
        ),
        _kpi_card(
            icon="triangle_alert",
            icon_background="#FFF7E6",
            icon_color="#D97706",
            label="Low Stock",
            value=InventoryState.low_stock_count,
            trend="+1 vs. last week",
            trend_background="#FEE2E2",
            trend_color="#DC2626",
            accent="#F59E0B",
        ),
        _kpi_card(
            icon="shopping_cart",
            icon_background="#EAF2FF",
            icon_color="#1D56D8",
            label="Orders",
            value=OrderState.total_orders,
            trend="+4 vs. last week",
            trend_background="#DCFCE7",
            trend_color="#15803D",
            accent="#1D56D8",
        ),
        class_name="inv-kpi-grid",
        width="100%",
    )
