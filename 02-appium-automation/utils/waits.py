"""
Explicit-wait helpers.

The ONLY waiting mechanism in this suite. We never call time.sleep() to wait for the UI —
we poll for a concrete condition (present / visible / clickable) and continue as soon as it
is true, which is both faster and far less flaky than a fixed sleep.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)

from utils.config_loader import load_config

_cfg = load_config()["timeouts"]
DEFAULT_TIMEOUT = _cfg["explicit"]
POLL = _cfg["polling"]


def _wait(driver, timeout=None):
    return WebDriverWait(
        driver,
        timeout or DEFAULT_TIMEOUT,
        poll_frequency=POLL,
        ignored_exceptions=(NoSuchElementException, StaleElementReferenceException),
    )


def wait_present(driver, by, value, timeout=None):
    return _wait(driver, timeout).until(EC.presence_of_element_located((by, value)))


def wait_visible(driver, by, value, timeout=None):
    return _wait(driver, timeout).until(EC.visibility_of_element_located((by, value)))


def wait_clickable(driver, by, value, timeout=None):
    return _wait(driver, timeout).until(EC.element_to_be_clickable((by, value)))


def is_visible(driver, by, value, timeout=5):
    """Non-throwing existence check — returns True/False."""
    try:
        wait_visible(driver, by, value, timeout)
        return True
    except TimeoutException:
        return False
