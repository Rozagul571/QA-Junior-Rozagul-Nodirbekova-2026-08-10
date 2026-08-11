"""Load config.yaml once and allow ENV overrides (UPPER_CASE keys)."""
import os
import functools
import yaml

_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")


@functools.lru_cache(maxsize=1)
def load_config():
    with open(_CONFIG_PATH, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)

    # Allow CI / local overrides without editing the file, e.g. DEVICE_NAME, APP_PATH.
    caps = cfg["capabilities"]
    for env_key, cap_key in {
        "DEVICE_NAME": "deviceName",
        "PLATFORM_VERSION": "platformVersion",
        "APP_PATH": "app",
        "APP_PACKAGE": "appPackage",
    }.items():
        if os.getenv(env_key):
            caps[cap_key] = os.getenv(env_key)

    if os.getenv("APPIUM_URL"):
        cfg["appium"]["server_url"] = os.getenv("APPIUM_URL")
    return cfg
