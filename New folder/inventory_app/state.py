"""Application state: authentication, inventory, cart, and orders."""

from __future__ import annotations

from datetime import datetime
from typing import Any, TypeAlias

import reflex as rx
from sqlmodel import select

from .models import (
    CATEGORIES,
    CartItem,
    Order,
    OrderItem,
    Product,
    format_currency,
    image_for_category,
    next_order_number,
    order_to_dict,
    product_to_dict,
    status_for_stock,
)

EventResult: TypeAlias = (
    rx.event.EventSpec | list[rx.event.EventSpec] | None
)


class AuthState(rx.State):
    """Session authentication and role-based route guards."""

    auth_user: str = rx.Cookie("", name="reflex_inventory_user")
    auth_role: str = rx.Cookie("", name="reflex_inventory_role")
    login_username: str = ""
    login_password: str = ""
    login_error: str = ""

    @rx.var
    def is_authenticated(self) -> bool:
        return bool(self.auth_user and self.auth_role)

    @rx.var
    def is_admin(self) -> bool:
        return self.auth_role == "admin"

    @rx.var
    def is_user(self) -> bool:
        return self.auth_role == "user"

    @rx.var
    def display_name(self) -> str:
        return "Administrator" if self.is_admin else "User"

    @rx.event
    def set_login_username(self, value: str) -> None:
        self.login_username = value
        self.login_error = ""

    @rx.event
    def set_login_password(self, value: str) -> None:
        self.login_password = value
        self.login_error = ""

    def _finish_login(self, username: str, role: str, message: str) -> EventResult:
        self.auth_user = username
        self.auth_role = role
        self.login_password = ""
        self.login_error = ""
        destination = "/admin" if role == "admin" else "/catalog"
        return [rx.toast.success(message), rx.redirect(destination)]

    @rx.event
    def login(self) -> EventResult:
        username = self.login_username.strip().lower()
        password = self.login_password
        if username == "admin" and password == "admin123":
            return self._finish_login("admin", "admin", "Welcome back, Administrator.")
        if username == "user" and password == "user123":
            return self._finish_login("user", "user", "Welcome back. Happy shopping!")
        self.login_error = "Invalid credentials. Use the demo buttons below or check the hints."
        return rx.toast.error("Invalid username or password.")

    @rx.event
    def demo_admin(self) -> EventResult:
        self.login_username = "admin"
        self.login_password = "admin123"
        return self._finish_login(
            "admin", "admin", "Signed in with the Administrator demo account."
        )

    @rx.event
    def demo_user(self) -> EventResult:
        self.login_username = "user"
        self.login_password = "user123"
        return self._finish_login(
            "user", "user", "Signed in with the User demo account."
        )

    @rx.event
    def logout(self) -> EventResult:
        self.auth_user = ""
        self.auth_role = ""
        self.login_username = ""
        self.login_password = ""
        return [rx.toast.info("You have been signed out."), rx.redirect("/login")]

    @rx.event
    def require_admin(self) -> EventResult:
        if not self.is_authenticated:
            return rx.redirect("/login")
        if not self.is_admin:
            return rx.redirect("/catalog")
        return None

    @rx.event
    def require_user(self) -> EventResult:
        if not self.is_authenticated:
            return rx.redirect("/login")
        return None

    @rx.event
    def guard_login(self) -> EventResult:
        if self.is_authenticated:
            return rx.redirect("/admin" if self.is_admin else "/catalog")
        return None

    @rx.event
    def guard_home(self) -> EventResult:
        if not self.is_authenticated:
            return rx.redirect("/login")
        return rx.redirect("/admin" if self.is_admin else "/catalog")


class InventoryState(rx.State):
    """Product CRUD, filtering, stock management, and KPI values."""

    search_query: str = ""
    status_filter: str = "All"
    form_name: str = ""
    form_sku: str = ""
    form_category: str = "Accessories"
    form_price: str = ""
    form_stock: str = "0"
    form_active: bool = True
    editing_id: int = 0
    last_poll: str = ""

    @rx.event
    def poll(self, date: str) -> None:
        self.last_poll = date

    @rx.event
    def set_search_query(self, value: str) -> None:
        self.search_query = value

    @rx.event
    def set_filter(self, value: str) -> None:
        self.status_filter = value

    @rx.event
    def set_form_name(self, value: str) -> None:
        self.form_name = value

    @rx.event
    def set_form_sku(self, value: str) -> None:
        self.form_sku = value

    @rx.event
    def set_form_category(self, value: str) -> None:
        self.form_category = value

    @rx.event
    def set_form_price(self, value: str) -> None:
        self.form_price = value

    @rx.event
    def set_form_stock(self, value: str) -> None:
        self.form_stock = value

    @rx.event
    def set_form_active(self, value: bool) -> None:
        self.form_active = value

    @rx.var(deps=["last_poll"])
    def products(self) -> list[dict[str, Any]]:
        with rx.session() as session:
            rows = session.exec(select(Product).order_by(Product.id)).all()
        return [product_to_dict(product) for product in rows]

    @rx.var(deps=["last_poll", "search_query", "status_filter"])
    def filtered_products(self) -> list[dict[str, Any]]:
        query = self.search_query.strip().lower()
        rows = self.products
        if query:
            rows = [
                product
                for product in rows
                if query in product["name"].lower()
                or query in product["sku"].lower()
                or query in product["category"].lower()
            ]
        if self.status_filter != "All":
            rows = [
                product
                for product in rows
                if product["status"] == self.status_filter
            ]
        return rows

    @rx.var(deps=["last_poll"])
    def active_products(self) -> list[dict[str, Any]]:
        return [product for product in self.products if product["is_active"]]

    @rx.var(deps=["last_poll"])
    def total_products(self) -> int:
        return len(self.products)

    @rx.var(deps=["last_poll"])
    def low_stock_count(self) -> int:
        return sum(1 for product in self.products if 1 <= product["stock"] <= 10)

    @rx.var(deps=["last_poll"])
    def in_stock_count(self) -> int:
        return sum(1 for product in self.products if 11 <= product["stock"] <= 49)

    @rx.var(deps=["last_poll"])
    def over_stock_count(self) -> int:
        return sum(1 for product in self.products if product["stock"] >= 50)

    @rx.var(deps=["last_poll"])
    def out_of_stock_count(self) -> int:
        return sum(1 for product in self.products if product["stock"] == 0)

    @rx.var
    def is_editing(self) -> bool:
        return self.editing_id > 0

    @rx.var
    def form_title(self) -> str:
        return "Edit Product" if self.is_editing else "Add Product"

    @rx.var
    def form_subtitle(self) -> str:
        return (
            "Update the selected product and save your changes."
            if self.is_editing
            else "Create a new product for your inventory."
        )

    @rx.var
    def save_label(self) -> str:
        return "Update Product" if self.is_editing else "Save Product"

    @rx.event
    def start_add(self) -> EventResult:
        self.editing_id = 0
        self.form_name = ""
        self.form_sku = ""
        self.form_category = "Accessories"
        self.form_price = ""
        self.form_stock = "0"
        self.form_active = True
        return rx.toast.info("Ready for a new product.")

    @rx.event
    def reset_form(self) -> EventResult:
        self.editing_id = 0
        self.form_name = ""
        self.form_sku = ""
        self.form_category = "Accessories"
        self.form_price = ""
        self.form_stock = "0"
        self.form_active = True
        return rx.toast.info("Product form reset.")

    @rx.event
    def edit_product(self, product_id: int) -> EventResult:
        with rx.session() as session:
            product = session.exec(
                select(Product).where(Product.id == product_id)
            ).first()
            if product is None:
                return rx.toast.error("That product no longer exists.")
            self.editing_id = product.id or 0
            self.form_name = product.name
            self.form_sku = product.sku
            self.form_category = product.category
            self.form_price = f"{product.price:.2f}"
            self.form_stock = str(product.stock)
            self.form_active = product.is_active
            return rx.toast.info(f"Editing {product.name}.")

    @rx.event
    def save_product(self) -> EventResult:
        name = self.form_name.strip()
        sku = self.form_sku.strip().upper()
        category = self.form_category.strip()
        if not name:
            return rx.toast.error("Product name is required.")
        if not sku:
            return rx.toast.error("SKU is required.")
        if category not in CATEGORIES:
            return rx.toast.error("Choose a valid product category.")
        try:
            price = float(self.form_price.replace("₱", "").replace("$", "").replace(",", "").strip())
        except ValueError:
            return rx.toast.error("Enter a valid price, for example 49.99.")
        try:
            stock = int(self.form_stock.strip())
        except ValueError:
            return rx.toast.error("Enter a valid whole-number stock quantity.")
        if price < 0:
            return rx.toast.error("Price cannot be negative.")
        if stock < 0:
            return rx.toast.error("Stock cannot be negative.")

        with rx.session() as session:
            duplicate = session.exec(
                select(Product).where(Product.sku == sku)
            ).first()
            if duplicate is not None and (duplicate.id or 0) != self.editing_id:
                return rx.toast.error(f"SKU {sku} is already in use.")

            if self.editing_id:
                product = session.exec(
                    select(Product).where(Product.id == self.editing_id)
                ).first()
                if product is None:
                    return rx.toast.error("That product no longer exists.")
                product.name = name
                product.sku = sku
                product.category = category
                product.price = round(price, 2)
                product.stock = stock
                product.is_active = self.form_active
                session.add(product)
                message = f"{name} updated successfully."
            else:
                product = Product(
                    name=name,
                    sku=sku,
                    category=category,
                    price=round(price, 2),
                    stock=stock,
                    is_active=self.form_active,
                    image=image_for_category(category),
                )
                session.add(product)
                message = f"{name} added to inventory."
            session.commit()

        self.editing_id = 0
        self.form_name = ""
        self.form_sku = ""
        self.form_category = "Accessories"
        self.form_price = ""
        self.form_stock = "0"
        self.form_active = True
        self.last_poll = datetime.now().isoformat()
        return rx.toast.success(message)

    @rx.event
    def delete_product(self, product_id: int) -> EventResult:
        with rx.session() as session:
            product = session.exec(
                select(Product).where(Product.id == product_id)
            ).first()
            if product is None:
                return rx.toast.error("That product was already removed.")
            name = product.name
            session.delete(product)
            session.commit()
        if self.editing_id == product_id:
            self.editing_id = 0
            self.form_name = ""
            self.form_sku = ""
            self.form_category = "Accessories"
            self.form_price = ""
            self.form_stock = "0"
            self.form_active = True
        self.last_poll = datetime.now().isoformat()
        return rx.toast.success(f"{name} deleted from inventory.")

    @rx.event
    def adjust_stock(self, product_id: int, delta: int) -> EventResult:
        with rx.session() as session:
            product = session.exec(
                select(Product).where(Product.id == product_id)
            ).first()
            if product is None:
                return rx.toast.error("That product no longer exists.")
            product.stock = max(0, product.stock + delta)
            session.add(product)
            session.commit()
            new_stock = product.stock
            name = product.name
        if self.editing_id == product_id:
            self.form_stock = str(new_stock)
        self.last_poll = datetime.now().isoformat()
        direction = "increased" if delta > 0 else "decreased"
        return rx.toast.success(f"{name} stock {direction} to {new_stock}.")

    @rx.event
    def toggle_active(self, product_id: int) -> EventResult:
        with rx.session() as session:
            product = session.exec(
                select(Product).where(Product.id == product_id)
            ).first()
            if product is None:
                return rx.toast.error("That product no longer exists.")
            product.is_active = not product.is_active
            session.add(product)
            session.commit()
            is_active = product.is_active
            name = product.name
        if self.editing_id == product_id:
            self.form_active = is_active
        self.last_poll = datetime.now().isoformat()
        state_label = "visible in" if is_active else "hidden from"
        return rx.toast.success(f"{name} is now {state_label} the catalog.")


class OrderState(rx.State):
    """Recent orders and order-status workflows."""

    last_poll: str = ""

    @rx.event
    def poll(self, date: str) -> None:
        self.last_poll = date

    @rx.var(deps=["last_poll"])
    def recent_orders(self) -> list[dict[str, Any]]:
        with rx.session() as session:
            rows = session.exec(
                select(Order).order_by(Order.created_at.desc()).limit(6)
            ).all()
        return [order_to_dict(order) for order in rows]

    @rx.var(deps=["last_poll"])
    def total_orders(self) -> int:
        with rx.session() as session:
            return len(session.exec(select(Order)).all())

    @rx.event
    def toggle_status(self, order_id: int) -> EventResult:
        with rx.session() as session:
            order = session.exec(select(Order).where(Order.id == order_id)).first()
            if order is None:
                return rx.toast.error("That order no longer exists.")
            order.status = (
                "Completed" if order.status == "Processing" else "Processing"
            )
            session.add(order)
            session.commit()
            number = order.order_number
            status = order.status
        self.last_poll = datetime.now().isoformat()
        return rx.toast.success(f"#ORD-{number.split('-')[-1]} marked {status}.")


class CartState(rx.State):
    """Per-session cart, stock validation, and checkout transaction."""

    cart: list[CartItem] = []
    last_poll: str = ""
    last_order_number: str = ""

    @rx.event
    def poll(self, date: str) -> None:
        self.last_poll = date

    @rx.var(deps=["last_poll", "cart"])
    def items(self) -> list[dict[str, Any]]:
        if not self.cart:
            return []
        with rx.session() as session:
            products = {
                product.id: product
                for product in session.exec(select(Product)).all()
            }
        rows: list[dict[str, Any]] = []
        for item in self.cart:
            product = products.get(item.product_id)
            if product is None:
                continue
            line_total = round(product.price * item.quantity, 2)
            in_stock = product.stock > 0
            rows.append(
                {
                    "product_id": item.product_id,
                    "name": product.name,
                    "sku": product.sku,
                    "category": product.category,
                    "price": product.price,
                    "price_display": format_currency(product.price),
                    "image": product.image,
                    "quantity": item.quantity,
                    "stock": product.stock,
                    "stock_label": (
                        f"In Stock ({product.stock} available)"
                        if in_stock
                        else "Out of Stock"
                    ),
                    "stock_bg": "#DCFCE7" if in_stock else "#FEE2E2",
                    "stock_color": "#15803D" if in_stock else "#DC2626",
                    "line_total": line_total,
                    "line_total_display": format_currency(line_total),
                    "can_increment": item.quantity < product.stock,
                }
            )
        return rows

    @rx.var(deps=["last_poll", "cart"])
    def item_count(self) -> int:
        return sum(item.quantity for item in self.cart)

    @rx.var(deps=["last_poll", "cart"])
    def subtotal(self) -> float:
        return round(sum(item["line_total"] for item in self.items), 2)

    @rx.var(deps=["last_poll", "cart"])
    def shipping(self) -> float:
        return 0.0

    @rx.var(deps=["last_poll", "cart"])
    def total(self) -> float:
        return round(self.subtotal + self.shipping, 2)

    @rx.var(deps=["last_poll", "cart"])
    def subtotal_display(self) -> str:
        return format_currency(self.subtotal)

    @rx.var(deps=["last_poll", "cart"])
    def shipping_display(self) -> str:
        return format_currency(self.shipping)

    @rx.var(deps=["last_poll", "cart"])
    def total_display(self) -> str:
        return format_currency(self.total)

    @rx.var(deps=["cart"])
    def cart_quantities(self) -> dict[int, int]:
        return {item.product_id: item.quantity for item in self.cart}

    @rx.var(deps=["last_poll", "cart"])
    def has_items(self) -> bool:
        return self.item_count > 0

    @rx.var(deps=["last_poll", "cart"])
    def cart_badge(self) -> str:
        return f"Cart: {self.item_count}"

    @rx.event
    def add_to_cart(self, product_id: int) -> EventResult:
        with rx.session() as session:
            product = session.exec(
                select(Product).where(Product.id == product_id)
            ).first()
            if product is None or not product.is_active:
                return rx.toast.error("This product is no longer available.")
            if product.stock <= 0:
                return rx.toast.warning(f"{product.name} is out of stock.")
            existing = next(
                (item for item in self.cart if item.product_id == product_id),
                None,
            )
            if existing is not None and existing.quantity >= product.stock:
                return rx.toast.warning(
                    f"Only {product.stock} unit(s) of {product.name} are available."
                )
            name = product.name
            if existing is not None:
                existing.quantity += 1
                existing.stock = product.stock
                existing.price = product.price
                existing.image = product.image
            else:
                self.cart = [
                    *self.cart,
                    CartItem(
                        product_id=product.id or 0,
                        name=product.name,
                        sku=product.sku,
                        category=product.category,
                        price=product.price,
                        stock=product.stock,
                        quantity=1,
                        image=product.image,
                    ),
                ]
        self.last_poll = datetime.now().isoformat()
        return rx.toast.success(f"{name} added to cart.")

    @rx.event
    def increment_quantity(self, product_id: int) -> EventResult:
        with rx.session() as session:
            product = session.exec(
                select(Product).where(Product.id == product_id)
            ).first()
            if product is None:
                return rx.toast.error("This product is no longer available.")
            item = next(
                (line for line in self.cart if line.product_id == product_id),
                None,
            )
            if item is None:
                return rx.toast.warning("That item is not in your cart.")
            if item.quantity >= product.stock:
                return rx.toast.warning(
                    f"Maximum available stock for {product.name} is {product.stock}."
                )
            item.quantity += 1
            item.stock = product.stock
            name = product.name
        self.last_poll = datetime.now().isoformat()
        return rx.toast.info(f"{name} quantity updated.")

    @rx.event
    def decrement_quantity(self, product_id: int) -> EventResult:
        item = next(
            (line for line in self.cart if line.product_id == product_id),
            None,
        )
        if item is None:
            return rx.toast.warning("That item is not in your cart.")
        name = item.name
        if item.quantity <= 1:
            self.cart = [
                line for line in self.cart if line.product_id != product_id
            ]
            self.last_poll = datetime.now().isoformat()
            return rx.toast.info(f"{name} removed from cart.")
        item.quantity -= 1
        self.last_poll = datetime.now().isoformat()
        return rx.toast.info(f"{name} quantity updated.")

    @rx.event
    def remove_item(self, product_id: int) -> EventResult:
        item = next(
            (line for line in self.cart if line.product_id == product_id),
            None,
        )
        if item is None:
            return rx.toast.warning("That item is not in your cart.")
        name = item.name
        self.cart = [
            line for line in self.cart if line.product_id != product_id
        ]
        self.last_poll = datetime.now().isoformat()
        return rx.toast.info(f"{name} removed from cart.")

    @rx.event
    def clear_cart(self) -> EventResult:
        if not self.cart:
            return rx.toast.info("Your cart is already empty.")
        self.cart = []
        self.last_poll = datetime.now().isoformat()
        return rx.toast.info("Cart cleared.")

    @rx.event
    async def checkout(self) -> EventResult:
        if not self.cart:
            return rx.toast.warning("Add at least one product before checking out.")

        with rx.session() as session:
            product_ids = [item.product_id for item in self.cart]
            products = {
                product.id: product
                for product in session.exec(
                    select(Product).where(Product.id.in_(product_ids))
                ).all()
            }
            for item in self.cart:
                product = products.get(item.product_id)
                if product is None or not product.is_active:
                    return rx.toast.error(
                        f"{item.name} is no longer available. Remove it from the cart."
                    )
                if product.stock < item.quantity:
                    return rx.toast.error(
                        f"Only {product.stock} unit(s) of {product.name} remain. "
                        "Update the cart quantity and try again."
                    )

            order_number = next_order_number(session)
            total = 0.0
            item_count = 0
            order = Order(
                order_number=order_number,
                item_count=0,
                total=0.0,
                status="Processing",
                created_at=datetime.now(),
            )
            session.add(order)
            session.flush()

            for item in self.cart:
                product = products[item.product_id]
                line_total = round(product.price * item.quantity, 2)
                total += line_total
                item_count += item.quantity
                product.stock = max(0, product.stock - item.quantity)
                session.add(product)
                session.add(
                    OrderItem(
                        order_id=order.id or 0,
                        product_id=product.id or 0,
                        product_name=product.name,
                        sku=product.sku,
                        quantity=item.quantity,
                        unit_price=product.price,
                        line_total=line_total,
                    )
                )
            order.item_count = item_count
            order.total = round(total, 2)
            session.add(order)
            session.commit()

        self.cart = []
        self.last_order_number = order_number
        self.last_poll = datetime.now().isoformat()

        inventory_state = await self.get_state(InventoryState)
        inventory_state.last_poll = datetime.now().isoformat()
        order_state = await self.get_state(OrderState)
        order_state.last_poll = datetime.now().isoformat()

        return rx.toast.success(
            f"Order #ORD-{order_number.split('-')[-1]} placed successfully. "
            "Inventory has been updated."
        )
