# 📱 Part 2 — Appium Automation (Python · Page Object Model)

Automated UI tests for the **Enatega Multivendor Customer** app.

- **Platform:** Android (UiAutomator2)
- **Language:** Python · **Runner:** pytest
- **Pattern:** Page Object Model
- **Waits:** explicit only (`WebDriverWait`) — no `time.sleep()`
- **Locators:** accessibility-id preferred, with resilient fallbacks — no absolute XPath
- **Screenshots:** captured automatically on any test failure

## Tests

| Test | File | Assertions |
|---|---|---|
| `test_successful_login` | `tests/test_login.py` | home search bar visible **+** profile tab present |
| `test_add_item_to_cart` | `tests/test_add_to_cart.py` | item present in cart **+** name matches **+** qty == 1 |

The two tests are **independent** — `test_add_item_to_cart` performs its own login, so tests
can run in any order or in isolation.

## Project structure

```
02-appium-automation/
├── pages/        # Page Objects: base_page, login, home, restaurant, cart
├── tests/        # test_login.py, test_add_to_cart.py, conftest.py (fixtures + hooks)
├── utils/        # driver_factory, waits (explicit), screenshots, config_loader
├── config/       # config.yaml (capabilities/timeouts/data) + locators.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## Prerequisites

- Node.js + **Appium 2** server: `npm i -g appium && appium driver install uiautomator2`
- Android SDK + a running emulator or a real device (`adb devices` shows it)
- Python 3.10+
- The app under test (`.apk`) — set its path in `config/config.yaml` (`capabilities.app`),
  or point `appPackage`/`appActivity` at an already-installed build.

## Setup & run

```bash
cd 02-appium-automation
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) start the Appium server in another terminal
appium

# 2) start an Android emulator / plug in a device, then:
pytest                      # runs all tests, writes report.html
pytest -m smoke             # only the login smoke test
pytest tests/test_add_to_cart.py::test_add_item_to_cart
```

Override device/app without editing files:

```bash
DEVICE_NAME="Pixel_7_API_34" APP_PATH="./app/enatega.apk" pytest
```

Outputs: `report.html` (pytest-html) and, on failure, PNGs under `screenshots/`.

## Design notes (mapping to the “green flags”)

| Green flag | Where |
|---|---|
| Accessibility-id locators | `config/locators.py` — primary strategy is `ACCESSIBILITY_ID` |
| Explicit waits | `utils/waits.py`; `implicitly_wait(0)` in `driver_factory.py` |
| Screenshot on failure | `tests/conftest.py` → `pytest_runtest_makereport` hook |
| Reusable methods | `pages/base_page.py` (`tap`, `type`, `text_of`, `is_displayed`) |
| Config separated | `config/config.yaml` (+ ENV overrides via `utils/config_loader.py`) |
| No test interdependence | each test logs in itself; `noReset: false` |

### About the locators (important)

At test time the Enatega build ships its controls **without** `testID` /
`accessibilityLabel` (documented as **BUG-002**). So each locator in `config/locators.py`
is an **ordered fallback**: the preferred `accessibility_id` first, then a resilient
UiAutomator/text locator that works on the current build. `BasePage._resolve()` picks the
first that matches — so the suite runs today and **automatically upgrades** to the fast,
stable accessibility-id path the moment the developers add the ids. No absolute XPath is
used anywhere.

**Recommended dev change** (makes automation and screen readers robust), e.g. in
`src/screens/Login/Login.js`:

```jsx
<TextInput testID="login_email_input" accessibilityLabel="login_email_input" ... />
<TouchableOpacity testID="login_continue_button" accessibilityLabel="login_continue_button" ... >
```
