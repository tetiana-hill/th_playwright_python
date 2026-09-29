import re

from playwright.sync_api import Locator, Page


class Header:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.get_by_test_id("title")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")

    def open_cart(self) -> None:
        self.page.get_by_test_id("shopping-cart-link").click()

    def logout(self) -> None:
        self.page.get_by_role("button", name="Open Menu").click()
        self.page.get_by_test_id("logout-sidebar-link").click()


class ProductList:
    """Product rows shared by the inventory, cart and checkout overview."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.rows = page.get_by_test_id("inventory-item")
        self.names = self.rows.get_by_test_id("inventory-item-name")
        self.prices = self.rows.get_by_test_id("inventory-item-price")

    def item(self, name: str) -> Locator:
        exact_name = self.page.get_by_test_id("inventory-item-name").filter(
            has_text=re.compile(rf"^{re.escape(name)}$")
        )
        return self.rows.filter(has=exact_name)

    def add(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Add to cart", exact=True).click()

    def remove(self, name: str) -> None:
        self.item(name).get_by_role("button", name="Remove", exact=True).click()
