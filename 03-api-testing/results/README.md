# Live API test run (results)

The **BONUS** folder of the Postman collection was executed live against the real Enatega
backend with Newman on 2026-08-10.

| File | What it is |
|---|---|
| `newman-live-run.txt` | Human-readable CLI output of the run |
| `newman-live-bonus.json` | Full machine-readable Newman report (requests + assertions + responses) |

**Result: 3 requests · 5 assertions · 0 failures.**

```
✓ Real backend has no REST /api/v1/auth/login (404)
✓ Server responded 400 for invalid variable type
✓ GraphQL validation error present
✓ HTTP 200 (GraphQL transport)
✓ No data / login is not granted
```

Reproduce:

```bash
newman run ../Enatega-Auth-Login.postman_collection.json \
  -e ../Enatega-Auth.postman_environment.json \
  --folder "2. BONUS — Live Enatega GraphQL API"
```
