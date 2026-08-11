"""
BasePage — reusable element interactions shared by every page object.

Key idea: locators are ordered fallback lists (see config/locators.py). `_resolve` returns
the first strategy that actually matches on the current build, so pages stay clean and the
suite survives the app not yet having accessibility ids (BUG-002) while preferring them.
All interactions go through EXPLICIT waits — no time.sleep().
"""
from selenium.common.exceptions import TimeoutException

from utils import waits


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    # -- locator resolution ---------------------------------------------------
    def _resolve(self, locator, timeout=None):
        """Return the first (by, value) in the fallback list that is present."""
        last_error = None
        for by, value in locator:
            try:
                waits.wait_present(self.driver, by, value, timeout or 6)
                return by, value
            except TimeoutException as exc:
                last_error = exc
                continue
        raise TimeoutException(f"None of the locators matched: {locator}") from last_error

    # -- interactions ---------------------------------------------------------
    def tap(self, locator):
        by, value = self._resolve(locator)
        waits.wait_clickable(self.driver, by, value).click()

    def type(self, locator, text):
        by, value = self._resolve(locator)
        el = waits.wait_visible(self.driver, by, value)
        el.clear()
        el.send_keys(text)

    def text_of(self, locator):
        by, value = self._resolve(locator)
        return waits.wait_visible(self.driver, by, value).text

    def is_displayed(self, locator, timeout=8):
        try:
            by, value = self._resolve(locator, timeout)
        except TimeoutException:
            return False
        return waits.is_visible(self.driver, by, value, timeout)

    def hide_keyboard_if_open(self):
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass  # not all drivers implement this; safe to ignore
