import pytest
from playwright.sync_api import Page, Playwright, expect

from pages.cart import CartPage
from pages.checkout import CheckoutPage
from pages.inventory import InventoryPage
from pages.login import LoginPage
from tests.data import BACKPACK, DEMO_PASSWORD, STANDARD_USER


@pytest.fixture(scope="session", autouse=True)
def configure_selectors(playwright: Playwright) -> None:
    playwright.selectors.set_test_id_attribute("data-test")
    expect.set_options(timeout=10_000)


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "viewport": {"width": 1440, "height": 900},
        "locale": "en-US",
    }


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.open()
    return login


@pytest.fixture
def inventory_page(login_page: LoginPage, page: Page) -> InventoryPage:
    login_page.login(STANDARD_USER, DEMO_PASSWORD)
    inventory = InventoryPage(page)
    expect(inventory.header.title).to_have_text("Products")
    expect(inventory.header.cart_badge).to_have_count(0)
    return inventory


@pytest.fixture
def checkout_page(inventory_page: InventoryPage, page: Page) -> CheckoutPage:
    inventory_page.products.add(BACKPACK.name)
    inventory_page.header.open_cart()
    CartPage(page).checkout()
    checkout = CheckoutPage(page)
    expect(checkout.header.title).to_have_text("Checkout: Your Information")
    return checkout
