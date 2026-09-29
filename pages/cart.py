from playwright.sync_api import Page

from pages.components import Header, ProductList


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = Header(page)
        self.products = ProductList(page)

    def checkout(self) -> None:
        self.page.get_by_test_id("checkout").click()

    def continue_shopping(self) -> None:
        self.page.get_by_test_id("continue-shopping").click()
