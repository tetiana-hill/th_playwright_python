from playwright.sync_api import Page

from pages.components import Header, ProductList


class InventoryPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = Header(page)
        self.products = ProductList(page)
        self.sort_select = page.get_by_test_id("product-sort-container")

    def sort_by(self, value: str) -> None:
        self.sort_select.select_option(value)
