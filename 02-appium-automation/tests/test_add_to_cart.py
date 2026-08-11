"""
Test 2 — test_add_item_to_cart

Login -> open restaurant -> add item to cart -> open cart -> verify item present.
Assertions (>= 2):
  1. The item is present in the cart
  2. The item name matches the one that was added
  3. (bonus) quantity is correct (== 1)

This test is INDEPENDENT of test_login: it performs its own login via the LoginPage
action, so the two tests can run in any order or in isolation. Screenshot-on-failure is
provided globally by the conftest hook.
"""
import pytest

from pages.login_page import LoginPage


@pytest.mark.regression
def test_add_item_to_cart(driver, config):
    data = config["test_data"]

    # own login -> no dependency on other tests
    home = LoginPage(driver).login(data["base_email"], data["password"])
    assert home.is_loaded(), "Precondition failed: home did not load after login"

    cart = (
        home.open_restaurant(data["restaurant_name"])
        .open_item(data["item_name"])
        .add_to_cart()
        .open_cart()
    )

    # Assertion 1 — item present in cart
    assert cart.is_item_present(data["item_name"]), (
        f"'{data['item_name']}' was not found in the cart after adding it"
    )

    # Assertion 2 — item name matches
    assert data["item_name"] in cart.item_name_text(data["item_name"]), (
        "Cart item name does not match the added item"
    )

    # Assertion 3 — quantity is correct
    assert cart.item_quantity(data["item_name"]) == 1, "Cart quantity should be 1"
