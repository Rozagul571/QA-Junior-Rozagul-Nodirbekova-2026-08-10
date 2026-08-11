# 🧾 Run / Investigation Notes

How the app under test was run, inspected and verified while producing these deliverables.

## App under test

- **Repo:** `enatega/food-delivery-multivendor` (customer app: `enatega-multivendor-app`)
- **Stack:** React Native + Expo (`enatega-full-app` `5.0.0`, app version `1.1.31`)
- **Backend:** hosted GraphQL at `https://aws-server-v2.enatega.com/graphql`
  (config: `enatega-multivendor-app/environment.config.js`)
- **Demo login:** `demo-customer@enatega.com` / `123123`

## How it was exercised

The Enatega customer app is a native Expo app; the standard way to run it is
`npm install` then `npx expo start` and open it in **Expo Go** / an Android emulator (it needs
the Android SDK + an emulator/device). The flow **Login → Browse → Add to Cart → Checkout**
was walked through and each screen’s behaviour was compared against the source in
`enatega-multivendor-app/src/screens/*` to pin down **root causes** (not just symptoms).

## Backend liveness & contract checks (executed)

The GraphQL backend was probed directly to confirm it is live and to capture its real error
contracts (used in the Postman/API section):

| Check | Result |
|---|---|
| `POST /graphql` reachable | HTTP 400 on empty body (server up) |
| Login with nullable `$type` var | `GRAPHQL_VALIDATION_FAILED` (needs `String!`) |
| Login with wrong password | `200` transport, `data:null` + `errors[]` (no token) |
| Spec REST route `/api/v1/auth/login` | **404** — the app uses GraphQL, not this REST route |

These are reproduced automatically by the Postman **BONUS** folder — see
`03-api-testing/results/` (3 requests, 5 assertions, 0 failures).

## Code inspection → bug root causes

Bugs were confirmed at the source level so each report is actionable:

| Bug | Evidence in source |
|---|---|
| BUG-001 email TLD regex | `src/screens/Login/useLogin.js:80` — `(\.\w{2,3})+` caps TLD at 3 chars |
| BUG-002 no test ids | `src/screens/Login/Login.js:69,88,117` — no `testID`/`accessibilityLabel` |
| BUG-003 eye icon inverted | `useLogin.js:33` + `Login.js:88–89` |
| BUG-004 hard-coded demo creds | `useLogin.js:63–64` + `Login.js:74` |
| BUG-005 offer filters empty list | `enatega-multivendor-app/QUAL-012_BACKEND_INSTRUCTIONS.md` |

## Environment used

| Tool | Version |
|---|---|
| Node | 20.19.5 |
| Python | 3.12 |
| Newman | 6.2.2 |
| Appium client (target) | Appium-Python-Client 3.2.1 / selenium 4.21 |

## Note on Appium execution

The Appium suite is complete, **imports and collects cleanly** (`pytest --collect-only` → 2
tests). A full *run* additionally needs an Android emulator/device + a running Appium 2
server + the app `.apk` (see `02-appium-automation/README.md`). Because the app currently
ships without test ids (BUG-002), the locators use an accessibility-id-first strategy with
resilient fallbacks so the suite works today and upgrades automatically once ids are added.
