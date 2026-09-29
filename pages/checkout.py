from playwright.sync_api import Page

from pages.components import Header, ProductList


class CheckoutPage:
    """The information, overview and confirmation steps of one checkout flow."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.header = Header(page)
        self.products = ProductList(page)
        self.error = page.get_by_test_id("error")
        self.subtotal = page.get_by_test_id("subtotal-label")
        self.tax = page.get_by_test_id("tax-label")
        self.total = page.get_by_test_id("total-label")
        self.confirmation = page.get_by_test_id("complete-header")

    def enter_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.page.get_by_test_id("firstName").fill(first_name)
        self.page.get_by_test_id("lastName").fill(last_name)
        self.page.get_by_test_id("postalCode").fill(postal_code)

    def continue_to_overview(self) -> None:
        self.page.get_by_test_id("continue").click()

    def cancel(self) -> None:
        self.page.get_by_test_id("cancel").click()

    def finish(self) -> None:
        self.page.get_by_test_id("finish").click()

    def back_home(self) -> None:
        self.page.get_by_test_id("back-to-products").click()
