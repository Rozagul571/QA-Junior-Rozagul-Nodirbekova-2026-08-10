"""
Test 1 — test_successful_login

Launch app -> enter valid credentials -> verify the Home screen loads.
Assertions (>= 2):
  1. Home search bar is visible  (home actually loaded)
  2. Profile tab is present      (authenticated navigation is rendered)
"""
import pytest

from pages.login_page import LoginPage


@pytest.mark.smoke
def test_successful_login(driver, config):
    creds = config["test_data"]

    home = LoginPage(driver).login(creds["base_email"], creds["password"])

    # Assertion 1 — the home/discovery screen has loaded
    assert home.is_loaded(), "Home screen did not load after login (search bar not visible)"

    # Assertion 2 — an authenticated navigation element is present
    assert home.is_profile_tab_visible(), "Profile tab is not visible after login"
