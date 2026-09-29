import re
from decimal import ROUND_HALF_UP, Decimal

import pytest
from playwright.sync_api import Page, expect

from pages.cart import CartPage
from pages.checkout import CheckoutPage
from pages.inventory import InventoryPage
from pages.login import LoginPage
from tests.data import BACKPACK, BIKE_LIGHT, DEMO_PASSWORD, STANDARD_USER


@pytest.mark.negative
@pytest.mark.parametrize(
    ("first_name", "last_name", "postal_code", "message"),
    [
        pytest.param("", "Customer", "12345", "Error: First Name is required", id="first-name"),
        pytest.param("Test", "", "12345", "Error: Last Name is required", id="last-name"),
        pytest.param("Test", "Customer", "", "Error: Postal Code is required", id="postal-code"),
    ],
)
def test_checkout_requires_customer_information(
    checkout_page: CheckoutPage,
    page: Page,
    first_name: str,
    last_name: str,
    postal_code: str,
    message: str,
) -> None:
    checkout_page.enter_information(first_name, last_name, postal_code)
    checkout_page.continue_to_overview()

    expect(checkout_page.error).to_have_text(message)
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
    expect(checkout_page.header.cart_badge).to_have_text("1")


def test_cancel_checkout_preserves_cart(checkout_page: CheckoutPage, page: Page) -> None:
    checkout_page.enter_information("Test", "Customer", "12345")

    checkout_page.cancel()

    cart = CartPage(page)
    expect(page).to_have_url(re.compile(r"/cart\.html$"))
    expect(cart.products.names).to_have_text([BACKPACK.name])
    expect(cart.header.cart_badge).to_have_text("1")


@pytest.mark.smoke
@pytest.mark.e2e
def test_customer_can_complete_two_product_purchase(login_page: LoginPage, page: Page) -> None:
    login_page.login(STANDARD_USER, DEMO_PASSWORD)
    inventory = InventoryPage(page)
    expect(inventory.header.title).to_have_text("Products")
    for product in (BACKPACK, BIKE_LIGHT):
        expect(
            inventory.products.item(product.name).get_by_test_id("inventory-item-price")
        ).to_have_text(product.price)
        inventory.products.add(product.name)
    inventory.header.open_cart()
    cart = CartPage(page)
    expect(cart.products.names).to_have_text([BACKPACK.name, BIKE_LIGHT.name])
    expect(cart.products.prices).to_have_text([BACKPACK.price, BIKE_LIGHT.price])
    expect(cart.products.rows.get_by_test_id("item-quantity")).to_have_text(["1", "1"])
    cart.checkout()
    checkout = CheckoutPage(page)
    checkout.enter_information("Test", "Customer", "12345")
    checkout.continue_to_overview()

    expect(checkout.header.title).to_have_text("Checkout: Overview")
    expect(checkout.products.names).to_have_text([BACKPACK.name, BIKE_LIGHT.name])
    expect(checkout.products.prices).to_have_text([BACKPACK.price, BIKE_LIGHT.price])
    expect(checkout.products.rows.get_by_test_id("item-quantity")).to_have_text(["1", "1"])
    # Independent demo price/tax expectations; Decimal avoids floating-point money errors.
    subtotal = Decimal("29.99") + Decimal("9.99")
    tax = (subtotal * Decimal("0.08")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    expect(checkout.subtotal).to_have_text(f"Item total: ${subtotal:.2f}")
    expect(checkout.tax).to_have_text(f"Tax: ${tax:.2f}")
    expect(checkout.total).to_have_text(f"Total: ${subtotal + tax:.2f}")

    checkout.finish()

    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))
    expect(checkout.confirmation).to_have_text("Thank you for your order!")
    expect(checkout.header.cart_badge).to_have_count(0)
    checkout.back_home()
    expect(inventory.header.title).to_have_text("Products")
    inventory.header.open_cart()
    expect(cart.products.rows).to_have_count(0)
