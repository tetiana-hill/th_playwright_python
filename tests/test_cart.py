from playwright.sync_api import Page, expect

from pages.cart import CartPage
from pages.inventory import InventoryPage
from tests.data import BACKPACK, BIKE_LIGHT


def test_cart_add_remove_keeps_product_and_badge_in_sync(
    inventory_page: InventoryPage, page: Page
) -> None:
    inventory_page.products.add(BACKPACK.name)
    inventory_page.products.add(BIKE_LIGHT.name)
    expect(inventory_page.header.cart_badge).to_have_text("2")
    inventory_page.header.open_cart()
    cart = CartPage(page)
    expect(cart.products.names).to_have_text([BACKPACK.name, BIKE_LIGHT.name])

    cart.products.remove(BACKPACK.name)

    expect(cart.products.names).to_have_text([BIKE_LIGHT.name])
    expect(cart.header.cart_badge).to_have_text("1")
    cart.products.remove(BIKE_LIGHT.name)
    expect(cart.products.rows).to_have_count(0)
    expect(cart.header.cart_badge).to_have_count(0)
    cart.continue_shopping()
    for product in (BACKPACK, BIKE_LIGHT):
        expect(
            inventory_page.products.item(product.name).get_by_role(
                "button", name="Add to cart", exact=True
            )
        ).to_be_visible()


def test_cart_survives_page_reload(inventory_page: InventoryPage, page: Page) -> None:
    inventory_page.products.add(BACKPACK.name)
    inventory_page.header.open_cart()

    page.reload()

    cart = CartPage(page)
    expect(cart.products.names).to_have_text([BACKPACK.name])
    expect(cart.products.prices).to_have_text([BACKPACK.price])
    expect(cart.products.item(BACKPACK.name).get_by_test_id("item-quantity")).to_have_text("1")
    expect(cart.header.cart_badge).to_have_text("1")
