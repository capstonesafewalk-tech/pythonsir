"""Reflex configuration for the Inventory & Ordering System."""

import reflex as rx

config = rx.Config(
    app_name="inventory_app",
    db_url="sqlite:///inventory.db",
)
