"""
pytest fixtures & hooks.

- `driver`  : a fresh Appium session per test (noReset=false => independent tests).
- screenshot-on-failure: the makereport hook captures a PNG whenever a test fails,
  satisfying the assignment's "Screenshot on failure" requirement for ALL tests.
"""
import os
import sys

import pytest

# make `pages`, `utils`, `config` importable regardless of the pytest CWD
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.driver_factory import create_driver          # noqa: E402
from utils.screenshots import save_screenshot           # noqa: E402
from utils.config_loader import load_config             # noqa: E402


@pytest.fixture()
def config():
    return load_config()


@pytest.fixture()
def driver(request):
    drv = create_driver()
    # expose the driver on the test node so the failure hook can screenshot it
    request.node._driver = drv
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the report when the test 'call' phase fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = getattr(item, "_driver", None)
        if drv is not None:
            path = save_screenshot(drv, f"FAILURE_{item.name}")
            if path:
                print(f"\n[screenshot-on-failure] saved: {path}")
