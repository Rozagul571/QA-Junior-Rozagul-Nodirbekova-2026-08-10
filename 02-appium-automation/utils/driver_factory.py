"""Builds an Appium driver from config — capabilities never live inside tests."""
from appium import webdriver
from appium.options.android import UiAutomator2Options

from utils.config_loader import load_config


def create_driver():
    """Create and return a fresh Appium Android driver using config.yaml."""
    cfg = load_config()
    options = UiAutomator2Options().load_capabilities(cfg["capabilities"])

    driver = webdriver.Remote(
        command_executor=cfg["appium"]["server_url"],
        options=options,
    )
    # Implicit wait stays at 0 on purpose — the whole suite uses EXPLICIT waits
    # (see utils/waits.py) so we never mix the two waiting strategies.
    driver.implicitly_wait(cfg["timeouts"]["implicit"])
    return driver
