"""Cart page object."""
from pages.base_page import BasePage
from config.locators import CartLocators


class CartPage(BasePage):
    def is_item_present(self, item_name):
        return self.is_displayed(CartLocators.cart_item_by_name(item_name))

    def item_name_text(self, item_name):
        return self.text_of(CartLocators.cart_item_by_name(item_name))

    def item_quantity(self, item_name):
        """Return the item's quantity as an int (digits parsed from the qty label)."""
        raw = self.text_of(CartLocators.cart_item_qty(item_name))
        digits = "".join(ch for ch in raw if ch.isdigit())
        return int(digits) if digits else 0
