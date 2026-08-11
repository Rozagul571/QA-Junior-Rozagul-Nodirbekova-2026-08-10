# 🧪 Test Cases — “Add to Cart” Feature

**Feature:** Add to Cart (Restaurant → Item → Cart)
**Tester:** Rozagul Nodirbekova  **Date:** 2026-08-10
**App:** Enatega Multivendor Customer `1.1.31` · Android 14 · Backend `aws-server-v2.enatega.com`

**Coverage:** 4 positive · 3 negative · 3 edge = **10 cases**
Priority legend — ![P1](https://img.shields.io/badge/-High-b30000) ![P2](https://img.shields.io/badge/-Medium-e67300) ![P3](https://img.shields.io/badge/-Low-999999)

**Global preconditions (unless noted):** user logged in as `demo-customer@enatega.com`, a
restaurant is **open**, network available, cart initially empty.

| ID | Type | Description | Preconditions | Steps | Expected Result | Priority |
|---|---|---|---|---|---|---|
| **TC-001** | ✅ Positive | Add a single available item to an empty cart | On a restaurant menu; cart empty | 1. Open “Pizza Palace”.<br>2. Tap **Margherita Pizza**.<br>3. Tap **Add to Cart**.<br>4. Open the cart. | Item appears in cart with qty **1**, correct name & price `$8.50`; cart badge shows **1**; subtotal = item price. | 🔴 High |
| **TC-002** | ✅ Positive | Increase quantity of an item from the item detail stepper | On item detail of Margherita Pizza | 1. Tap **+** on the quantity stepper twice (qty = 3).<br>2. Tap **Add to Cart**.<br>3. Open cart. | Cart shows Margherita Pizza qty **3**; line total = `3 × $8.50 = $25.50`; subtotal updates accordingly. | 🔴 High |
| **TC-003** | ✅ Positive | Add two different items from the same restaurant | On “Pizza Palace” menu; cart empty | 1. Add **Margherita Pizza**.<br>2. Go back, add **Pepperoni Pizza**.<br>3. Open cart. | Cart lists **both** items with correct individual prices; subtotal = sum of both; item count = 2. | 🔴 High |
| **TC-004** | ✅ Positive | Cart persists after backgrounding the app | Item already in cart | 1. Add an item.<br>2. Background the app (Home), wait 30 s.<br>3. Re-open the app. | Cart still contains the item with the same qty and price; nothing is lost. | 🟠 Medium |
| **TC-005** | ⛔ Negative | Add item from a **different** restaurant while a cart exists | Cart already has an item from “Pizza Palace” | 1. Go to “Burger Hub”.<br>2. Add **Cheeseburger**.<br>3. Observe the prompt. | App warns that a new cart will replace the current one and asks to confirm (**Clear & add** / **Cancel**); cart integrity is preserved — no silent mixing of two restaurants. | 🔴 High |
| **TC-006** | ⛔ Negative | Add an **out-of-stock / unavailable** item | Menu shows an item marked *Unavailable* | 1. Locate an unavailable item.<br>2. Attempt to tap **Add to Cart**. | The Add button is disabled (or a clear “Currently unavailable” message shows); item is **not** added; cart unchanged. | 🟠 Medium |
| **TC-007** | ⛔ Negative | Add to cart while **offline** | Item detail open; then disable network | 1. Enable Airplane mode.<br>2. Tap **Add to Cart**. | A clear connectivity error is shown and the cart is not silently corrupted; on reconnect the action can be retried. | 🟠 Medium |
| **TC-008** | 🔶 Edge | Decrease quantity to **0** from the cart | Cart has one item, qty 1 | 1. Open cart.<br>2. Tap **–** on the item until qty reaches 0. | Item is removed and a confirmation/undo appears; if it was the last item the empty-cart state is shown; no negative quantities. | 🟠 Medium |
| **TC-009** | 🔶 Edge | Add a very large quantity of one item | On item detail | 1. Increase quantity to **99**.<br>2. Tap **Add to Cart**.<br>3. Open cart. | Quantity is capped at a sane maximum (or accepted with correct math); line total = `qty × price` with no overflow/`NaN`; UI stays aligned. | 🟡 Low |
| **TC-010** | 🔶 Edge | Add an item with **required customisation** without selecting options | Item has a mandatory option group (e.g. size) | 1. Open the customisable item.<br>2. Tap **Add to Cart** without choosing the required option. | App blocks the add and highlights the required option group with a message; item is not added until a valid selection is made. | 🟠 Medium |

---

### 🔁 Traceability

| Test Case | Verifies / relates to |
|---|---|
| TC-005 | Single-restaurant cart rule (common food-delivery constraint) |
| TC-006, TC-007 | Robustness — unavailable item & offline handling |
| TC-008, TC-009 | Quantity boundary behaviour |
| TC-010 | Required-modifier validation |

> 📄 A colour-coded PDF export of this table is in **`docs/pdf/test-cases.pdf`**.
