# Live API test run (results)

The **live backend** folder of the Postman collection was executed with Newman against the
real Enatega backend on 2026-08-10.

| File | What it is |
|---|---|
| `newman-live-report.html` | Rich HTML report (htmlextra) — open in a browser |
| `newman-live-run.txt` | Human-readable CLI output |
| `newman-live-bonus.json` | Full machine-readable Newman report |
| `../screenshots/postman-live-run.png` | Screenshot of the passing run |
| `../../docs/pdf/api-postman-run-report.pdf` | PDF of the report |

**Result: 5 requests · 10 assertions · 0 failures.**

```
✓ Health — GraphQL up (__typename) → 200 + data
✓ Spec REST route on real backend → 404
✓ GraphQL login — invalid variable type → 400 (GRAPHQL_VALIDATION_FAILED)
✓ GraphQL login — wrong password → no token
✓ Protected query without token → Unauthorized
```

Reproduce:

```bash
newman run ../Enatega-Auth-Login.postman_collection.json \
  -e ../Enatega-Auth.postman_environment.json \
  --folder "2. Live backend — real Enatega GraphQL" \
  -r cli,htmlextra
```
