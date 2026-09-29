from decimal import Decimal

import pytest
from playwright.sync_api import expect

from pages.inventory import InventoryPage


@pytest.mark.parametrize(
    ("option", "descending"), [("lohi", False), ("hilo", True)], ids=["low-to-high", "high-to-low"]
)
def test_sort_products_by_price(
    inventory_page: InventoryPage, option: str, descending: bool
) -> None:
    prices = inventory_page.products.prices
    expect(prices).to_have_count(6)
    original_prices = prices.all_text_contents()
    expected = sorted(
        original_prices, key=lambda price: Decimal(price.lstrip("$")), reverse=descending
    )

    inventory_page.sort_by(option)

    expect(inventory_page.sort_select).to_have_value(option)
    expect(prices).to_have_text(expected)


@pytest.mark.parametrize(
    ("option", "descending"), [("az", False), ("za", True)], ids=["a-to-z", "z-to-a"]
)
def test_sort_products_by_name(
    inventory_page: InventoryPage, option: str, descending: bool
) -> None:
    names = inventory_page.products.names
    expect(names).to_have_count(6)
    expected = sorted(names.all_text_contents(), reverse=descending)
    # Start from the opposite order so even the default A-Z option must change the list.
    inventory_page.sort_by("az" if descending else "za")
    expect(names).to_have_text(list(reversed(expected)))

    inventory_page.sort_by(option)

    expect(inventory_page.sort_select).to_have_value(option)
    expect(names).to_have_text(expected)
