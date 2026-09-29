import re

import pytest
from playwright.sync_api import Page, expect

from pages.inventory import InventoryPage
from pages.login import LoginPage
from tests.data import DEMO_PASSWORD, STANDARD_USER


@pytest.mark.smoke
def test_standard_user_can_log_in(login_page: LoginPage, page: Page) -> None:
    login_page.login(STANDARD_USER, DEMO_PASSWORD)

    inventory = InventoryPage(page)
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory.header.title).to_have_text("Products")
    expect(inventory.products.rows).to_have_count(6)


@pytest.mark.negative
@pytest.mark.parametrize(
    ("username", "password", "message"),
    [
        pytest.param(
            STANDARD_USER,
            "incorrect-password",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid-password",
        ),
        pytest.param(
            "locked_out_user",
            DEMO_PASSWORD,
            "Epic sadface: Sorry, this user has been locked out.",
            id="locked-out-user",
        ),
        pytest.param("", DEMO_PASSWORD, "Epic sadface: Username is required", id="empty-username"),
        pytest.param(STANDARD_USER, "", "Epic sadface: Password is required", id="empty-password"),
    ],
)
def test_login_rejects_invalid_input(
    login_page: LoginPage, page: Page, username: str, password: str, message: str
) -> None:
    login_page.login(username, password)

    expect(login_page.error).to_have_text(message)
    expect(login_page.login_button).to_be_visible()
    expect(InventoryPage(page).products.rows).to_have_count(0)


def test_logout_prevents_inventory_reentry(inventory_page: InventoryPage, page: Page) -> None:
    inventory_page.header.logout()
    expect(LoginPage(page).login_button).to_be_visible()

    page.goto("/inventory.html")

    expect(LoginPage(page).error).to_contain_text("You can only access")
    expect(inventory_page.products.rows).to_have_count(0)


@pytest.mark.negative
def test_anonymous_user_cannot_open_inventory(page: Page) -> None:
    page.goto("/inventory.html")

    expect(LoginPage(page).login_button).to_be_visible()
    expect(LoginPage(page).error).to_have_text(
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
    )
    expect(InventoryPage(page).products.rows).to_have_count(0)
