"""Main Reflex application module."""

from __future__ import annotations

import reflex as rx

from .models import init_db
from .state import AuthState

from .pages.admin import admin_page
from .pages.catalog import catalog_page
from .pages.login import login_page

init_db()

app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
        gray_color="slate",
        radius="medium",
        scaling="90%",
    ),
    stylesheets=["/styles.css"],
)


@rx.page(route="/", on_load=AuthState.guard_home)
def home_page() -> rx.Component:
    """Redirect the root route to the role-appropriate destination."""

    return rx.fragment()
