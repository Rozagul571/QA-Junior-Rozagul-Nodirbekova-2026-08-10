# 🔌 Part 3 — API Testing (Postman)

**Author:** Rozagul Nodirbekova · **Date:** 2026-08-10

## Files

| File | Purpose |
|---|---|
| `Enatega-Auth-Login.postman_collection.json` | The collection (import into Postman / run with Newman) |
| `Enatega-Auth.postman_environment.json` | Environment with `base_url`, `graphql_host`, `auth_token` |

## Endpoint under test (per assignment)

```http
POST {{base_url}}/api/v1/auth/login
Content-Type: application/json

{
  "phone_number": "+998901234567",
  "otp_code": "123456"
}
```

`base_url` is an **environment variable** so the same collection runs against any conforming
server, a Postman **mock server**, or a local backend — no hard-coded hosts.

## Test matrix

| # | Case | Request | Expected status | Key assertions |
|---|---|---|---|---|
| 1 | ✅ Positive | valid phone + valid OTP | `200` | JSON body; non-empty `token` (saved to env); response < 2 s |
| 2 | ⛔ Negative | invalid OTP (`000000`) | `401` | no `token`; error message matches `/otp\|code\|invalid/` |
| 3 | ⛔ Negative | missing `phone_number` | `400` | error names the `phone` field; no `token` |
| 4 | ⛔ Negative | invalid phone format (`12345`) | `400` or `422` | error mentions format/validation; no `token` |

### Bonus — live tests against the real backend (`aws-server-v2.enatega.com`)

The customer app does **not** use a REST `/api/v1/auth/login` route — it authenticates over
**GraphQL**. The collection documents and proves this with live requests:

| # | Case | Result |
|---|---|---|
| 5 | REST spec route on real backend | `404` (route does not exist) — documented finding |
| 6 | GraphQL login with wrong variable type | `400` + `GRAPHQL_VALIDATION_FAILED` |
| 7 | GraphQL login with wrong password | `200` transport, `data:null` + `errors[]` (no token) |

> These three were **executed live** while writing this suite; the responses shown in
> `results/` were captured from the real server.

## How to run

**In Postman (UI):**
1. Import both JSON files (Collection + Environment).
2. Select the *Enatega — Auth (env)* environment (top-right).
3. Set `base_url` to your server (or a Postman mock) and click **Run** on the collection.

**From the CLI with Newman:**
```bash
npm install -g newman
newman run Enatega-Auth-Login.postman_collection.json \
  -e Enatega-Auth.postman_environment.json \
  --reporters cli,json --reporter-json-export results/newman-report.json
```

## Notes on quality

- Every request has **explicit assertions** (status + body + error message), not just a “send”.
- The positive test **chains** the returned token into `{{auth_token}}` for downstream requests.
- Tests are **resilient**: negative tests assert the *absence* of a token, and messages are
  matched with case-insensitive regex so minor wording changes don’t cause false failures.
