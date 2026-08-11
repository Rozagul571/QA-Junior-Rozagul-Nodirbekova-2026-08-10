"""
Centralised locators — one place to change when the UI changes.

LOCATOR STRATEGY (see README + BUG-002)
---------------------------------------
The assignment's green flags ask for **accessibility-id locators** and forbid absolute
XPath. The correct, stable strategy is therefore `ACCESSIBILITY_ID`, which on Android maps
to a view's `content-desc` and comes from a React Native `accessibilityLabel` / `testID`.

At the time of testing the Enatega app ships those controls WITHOUT test ids
(filed as BUG-002). So each locator below is expressed as an **ordered fallback list**:

    1. ACCESSIBILITY_ID  — the target the dev team should expose (preferred)
    2. a resilient UiAutomator/text locator that works on the current build

`BasePage` tries them in order, so the suite runs today AND automatically upgrades to the
fast, stable accessibility-id path the moment the devs add the ids — no test changes needed.
No absolute XPath is used anywhere.
"""
from appium.webdriver.common.appiumby import AppiumBy

# Each value is a tuple: (primary_locator, *fallback_locators)
# where a locator is itself a (by, value) tuple.


class LoginLocators:
    EMAIL_INPUT = (
        (AppiumBy.ACCESSIBILITY_ID, "login_email_input"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)'),
    )
    PASSWORD_INPUT = (
        (AppiumBy.ACCESSIBILITY_ID, "login_password_input"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)'),
    )
    CONTINUE_BTN = (
        (AppiumBy.ACCESSIBILITY_ID, "login_continue_button"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)continue")'),
    )
    LOGIN_BTN = (
        (AppiumBy.ACCESSIBILITY_ID, "login_submit_button"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textMatches("(?i)log ?in")'),
    )
    EMAIL_ERROR = (
        (AppiumBy.ACCESSIBILITY_ID, "login_email_error"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("valid email")'),
    )


class HomeLocators:
    # Elements that prove the authenticated Home/Discovery screen has loaded.
    SEARCH_BAR = (
        (AppiumBy.ACCESSIBILITY_ID, "home_search_input"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Search")'),
    )
    PROFILE_TAB = (
        (AppiumBy.ACCESSIBILITY_ID, "tab_profile"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Profile")'),
    )
    CART_TAB = (
        (AppiumBy.ACCESSIBILITY_ID, "tab_cart"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Cart")'),
    )

    @staticmethod
    def restaurant_by_name(name):
        return (
            (AppiumBy.ACCESSIBILITY_ID, f"restaurant_card_{name}"),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{name}")'),
        )


class RestaurantLocators:
    @staticmethod
    def item_by_name(name):
        return (
            (AppiumBy.ACCESSIBILITY_ID, f"menu_item_{name}"),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{name}")'),
        )

    ADD_TO_CART_BTN = (
        (AppiumBy.ACCESSIBILITY_ID, "item_add_to_cart_button"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Add to Cart")'),
    )
    QTY_PLUS = (
        (AppiumBy.ACCESSIBILITY_ID, "item_qty_increment"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("increase")'),
    )


class CartLocators:
    OPEN_CART = (
        (AppiumBy.ACCESSIBILITY_ID, "tab_cart"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Cart")'),
    )
    SUBTOTAL = (
        (AppiumBy.ACCESSIBILITY_ID, "cart_subtotal"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Subtotal")'),
    )
    CHECKOUT_BTN = (
        (AppiumBy.ACCESSIBILITY_ID, "cart_checkout_button"),
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Checkout")'),
    )

    @staticmethod
    def cart_item_by_name(name):
        return (
            (AppiumBy.ACCESSIBILITY_ID, f"cart_item_{name}"),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{name}")'),
        )

    @staticmethod
    def cart_item_qty(name):
        return (
            (AppiumBy.ACCESSIBILITY_ID, f"cart_item_qty_{name}"),
            (AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().descriptionContains("{name} quantity")'),
        )
