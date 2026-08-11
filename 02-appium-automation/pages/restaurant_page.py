"""Restaurant menu / item detail page object."""
from pages.base_page import BasePage
from pages.cart_page import CartPage
from config.locators import RestaurantLocators, CartLocators


class RestaurantPage(BasePage):
    def open_item(self, item_name):
        self.tap(RestaurantLocators.item_by_name(item_name))
        return self

    def add_to_cart(self):
        self.tap(RestaurantLocators.ADD_TO_CART_BTN)
        return self

    def open_cart(self):
        self.tap(CartLocators.OPEN_CART)
        return CartPage(self.driver)
