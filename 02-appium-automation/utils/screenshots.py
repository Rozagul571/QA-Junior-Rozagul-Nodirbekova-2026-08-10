"""Screenshot helper — used by the pytest hook to capture the screen on failure."""
import os
import time

from utils.config_loader import load_config


def save_screenshot(driver, name):
    """Save a PNG under the configured screenshots dir; returns the file path."""
    out_dir = load_config()["paths"]["screenshots"]
    os.makedirs(out_dir, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
    path = os.path.join(out_dir, f"{safe}_{time.strftime('%Y%m%d-%H%M%S')}.png")
    try:
        driver.save_screenshot(path)
    except Exception:  # never let screenshotting mask the real test failure
        return None
    return path
