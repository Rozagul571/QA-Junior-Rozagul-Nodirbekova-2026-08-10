"""Login page object — models the real Enatega two-step email → password flow."""
from pages.base_page import BasePage
from pages.home_page import HomePage
from config.locators import LoginLocators


class LoginPage(BasePage):
    """Enatega logs in as: enter email -> Continue -> enter password -> Login."""

    def enter_email(self, email):
        self.type(LoginLocators.EMAIL_INPUT, email)
        self.hide_keyboard_if_open()
        return self

    def tap_continue(self):
        self.tap(LoginLocators.CONTINUE_BTN)
        return self

    def enter_password(self, password):
        self.type(LoginLocators.PASSWORD_INPUT, password)
        self.hide_keyboard_if_open()
        return self

    def tap_login(self):
        self.tap(LoginLocators.LOGIN_BTN)
        return HomePage(self.driver)

    def login(self, email, password):
        """High-level, reusable action: full happy-path login -> returns HomePage."""
        self.enter_email(email).tap_continue()
        self.enter_password(password)
        return self.tap_login()

    # negative-path helper
    def email_error_text(self):
        return self.text_of(LoginLocators.EMAIL_ERROR)
