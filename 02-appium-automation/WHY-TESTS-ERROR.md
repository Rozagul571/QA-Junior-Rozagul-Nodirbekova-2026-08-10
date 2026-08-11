# Why the two Appium tests show ERROR — and what a QA does about it

When you ran `pytest`, both tests ended in **ERROR** (not FAIL) with:

```
urllib3.exceptions.MaxRetryError: HTTPConnectionPool(host='127.0.0.1', port=4723):
Max retries exceeded with url: /session
(Caused by NewConnectionError('... [Errno 111] Connection refused'))
```

## What this means (read the error, don't panic)

- The failure happens in **setup** (`ERROR`), before any test assertion runs. That already
  tells you it is an **environment / prerequisite** problem, not a bug in the test logic.
- `127.0.0.1:4723` is the **Appium server** address. `Connection refused` = **nothing is
  listening there** → the Appium server is not running.
- Earlier in your log: `appium: command not found` — the Appium 2 server was never installed
  (the `npm i -g appium` was cancelled with Ctrl-C). So there is no server, and also no
  Android emulator/device for it to drive.

So the chain that must exist for a mobile UI test to run is:

```
pytest  →  Appium client (Python)  →  Appium server (:4723)  →  UiAutomator2  →  Android emulator/device  →  the app (.apk)
                                        ❌ missing              ❌ missing        ❌ missing
```

Only the first link exists on this machine, so the session can’t be created.

## This is NOT a code defect

`ERROR at setup` with `Connection refused` is a **classic environment blocker**. The test
**code itself is valid** — it was proven by:

```
pytest --collect-only  →  collected 2 items   (imports, fixtures, page objects all OK)
```

A QA never reports “tests are broken” here. A QA reports: **“test environment not provisioned:
Appium server + Android emulator missing.”**

## What a QA actually does (the process)

1. **Triage the signal.** Distinguish *product defect* vs *environment problem* vs *test-code
   bug*. `Connection refused` in setup ⇒ environment problem → this does **not** go in the bug
   tracker as an app bug; it goes in the **test run report** as a blocked/not-run result.

2. **Mark the run correctly.** In the test report the two tests are **BLOCKED / Not Run**
   (prerequisite unmet), not **Failed**. Failing ≠ blocked — mixing them corrupts pass-rate
   metrics.

3. **Provision the environment** (the actual fix), then re-run:
   ```bash
   # 1) install & start the Appium 2 server
   npm i -g appium
   appium driver install uiautomator2
   appium                       # leave running on :4723

   # 2) start an Android emulator (or plug in a device)
   emulator -avd Pixel_6_API_34   # or: adb devices  → shows a device

   # 3) point config at the app and run
   cd 02-appium-automation && source .venv/bin/activate
   #   set capabilities.app / appPackage in config/config.yaml
   pytest
   ```

4. **Report the blocker to the team** with the exact cause and the unblock steps (above), so
   it is actionable — same standard as any bug report.

## Where these blockers are listed

They are also captured in the project-level map: `../BUG-LOCATION-MAP.md` → **⬛ Build/Env
layer (E1–E4)**: PEP 668 venv, Appium not installed, no server/emulator, disk full.

## Summary

| Question | Answer |
|---|---|
| Is the test code broken? | No — `--collect-only` collects both tests; failure is in setup. |
| What failed? | Creating an Appium session — server on `:4723` is not running. |
| Root cause | Appium server not installed/started + no Android emulator/device. |
| Bug or environment? | **Environment** — report as *blocked*, not as an app defect. |
| Fix | Install & start Appium, boot an emulator/device, set the app path, re-run. |
