"""Home / Discovery page object — the authenticated landing screen."""
from pages.base_page import BasePage
from pages.restaurant_page import RestaurantPage
from config.locators import HomeLocators


class HomePage(BasePage):
    def is_loaded(self):
        """Home is considered loaded when the search bar is visible."""
        return self.is_displayed(HomeLocators.SEARCH_BAR)

    def is_profile_tab_visible(self):
        return self.is_displayed(HomeLocators.PROFILE_TAB)

    def open_restaurant(self, name):
        self.tap(HomeLocators.restaurant_by_name(name))
        return RestaurantPage(self.driver)
