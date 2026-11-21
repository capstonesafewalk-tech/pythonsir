"""Fixed dark-navy admin sidebar."""

from __future__ import annotations

import reflex as rx

from ..state import OrderState

NAVY = "#132B55"
BLUE = "#1D56D8"


def _nav_item(
    icon: str,
    label: str,
    href: str,
    *,
    active: bool = False,
    badge: rx.Component | None = None,
) -> rx.Component:
    classes = "inv-nav-link inv-nav-link-active" if active else "inv-nav-link"
    return rx.el.a(
        rx.hstack(
            rx.icon(icon, size=19, stroke_width=2),
            rx.el.span(label, class_name="inv-sidebar-label"),
            rx.spacer(),
            badge,
            width="100%",
            align="center",
            spacing="3",
        ),
        href=href,
        class_name=classes,
        display="flex",
        align="center",
        width="100%",
        padding="11px 14px",
        border_radius="10px",
        color="#D7E4F8" if not active else "#FFFFFF",
        font_size="14px",
        font_weight="600",
        text_decoration="none",
    )


def sidebar() -> rx.Component:
    """Render the admin navigation shell."""

    return rx.el.aside(
        rx.vstack(
            rx.hstack(
                rx.box(
                    rx.image(
                        src="/brand/cube.svg",
                        alt="KonektPC",
                        width="42px",
                        height="42px",
                    ),
                    width="46px",
                    height="46px",
                    border_radius="13px",
                    background="rgba(96, 165, 250, 0.14)",
                    border="1px solid rgba(147, 197, 253, 0.2)",
                    display="flex",
                    align="center",
                    justify="center",
                    flex_shrink="0",
                ),
                rx.vstack(
                    rx.text(
                        "KonektPC",
                        color="#FFFFFF",
                        font_size="16px",
                        font_weight="800",
                        letter_spacing="-0.02em",
                        line_height="1.2",
                        class_name="inv-sidebar-brand-text",
                    ),
                    rx.text(
                        "PC Parts & Ordering System",
                        color="#9DB5D8",
                        font_size="10px",
                        font_weight="500",
                        line_height="1.3",
                        class_name="inv-sidebar-brand-text",
                    ),
                    spacing="0",
                    align="start",
                ),
                spacing="3",
                align="center",
                width="100%",
                padding="2px 8px 0",
            ),
            rx.el.div(
                width="100%",
                height="1px",
                background="rgba(148, 163, 184, 0.18)",
                margin="24px 0 18px",
            ),
            rx.vstack(
                _nav_item(
                    "layout_dashboard",
                    "Dashboard",
                    "/admin",
                    active=True,
                ),
                _nav_item("package", "Inventory", "#inventory"),
                _nav_item(
                    "shopping_cart",
                    "Orders",
                    "#orders",
                    badge=rx.el.span(
                        OrderState.total_orders,
                        class_name="inv-sidebar-badge",
                        background="rgba(96, 165, 250, 0.18)",
                        color="#BFDBFE",
                        border="1px solid rgba(147, 197, 253, 0.2)",
                        border_radius="999px",
                        padding="2px 8px",
                        font_size="11px",
                        font_weight="700",
                        min_width="24px",
                        text_align="center",
                    ),
                ),
                rx.el.button(
                    rx.hstack(
                        rx.icon("bar_chart_3", size=19),
                        rx.el.span("Analytics", class_name="inv-sidebar-label"),
                        width="100%",
                        align="center",
                        spacing="3",
                    ),
                    on_click=rx.toast.info("Analytics summary is shown in the KPI cards."),
                    class_name="inv-nav-link",
                    width="100%",
                    padding="11px 14px",
                    border="none",
                    border_radius="10px",
                    background="transparent",
                    color="#D7E4F8",
                    font_size="14px",
                    font_weight="600",
                ),
                rx.el.button(
                    rx.hstack(
                        rx.icon("settings", size=19),
                        rx.el.span("Settings", class_name="inv-sidebar-label"),
                        width="100%",
                        align="center",
                        spacing="3",
                    ),
                    on_click=rx.toast.info("Use the product form and inventory switches to manage settings."),
                    class_name="inv-nav-link",
                    width="100%",
                    padding="11px 14px",
                    border="none",
                    border_radius="10px",
                    background="transparent",
                    color="#D7E4F8",
                    font_size="14px",
                    font_weight="600",
                ),
                spacing="2",
                width="100%",
            ),
            rx.spacer(),
            rx.vstack(
                rx.el.div(
                    width="100%",
                    height="1px",
                    background="rgba(148, 163, 184, 0.18)",
                    margin="0 0 16px",
                ),
                rx.hstack(
                    rx.image(
                        src="/brand/python.svg",
                        alt="Python",
                        width="30px",
                        height="30px",
                    ),
                    rx.vstack(
                        rx.text(
                            "Built with",
                            color="#8FA9CD",
                            font_size="10px",
                            line_height="1.2",
                            class_name="inv-sidebar-footer-text",
                        ),
                        rx.text(
                            "Python Reflex",
                            color="#D7E4F8",
                            font_size="12px",
                            font_weight="700",
                            line_height="1.2",
                            class_name="inv-sidebar-footer-text",
                        ),
                        spacing="0",
                        align="start",
                    ),
                    spacing="3",
                    align="center",
                    padding="0 8px",
                ),
                width="100%",
                padding="0 0 4px",
            ),
            height="100vh",
            width="100%",
            spacing="0",
            padding="26px 18px 22px",
            align="start",
        ),
        class_name="inv-sidebar",
    )
