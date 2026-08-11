#!/usr/bin/env python3
"""
Generate annotated UI mockup screenshots for the QA deliverables.

These are clean, labelled *reference mockups* of the Enatega customer app
(Login -> Browse -> Add to Cart -> Checkout) used to illustrate the manual
test cases and bug reports. They are drawn programmatically with Pillow so the
documentation is self-contained and reproducible. On a real device run they
would be replaced 1:1 by device captures (same file names).

Usage:  python3 scripts/generate_screenshots.py
Output: 01-manual-testing/screenshots/*.png
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(__file__), "..", "01-manual-testing", "screenshots")
os.makedirs(OUT, exist_ok=True)

# ---- palette (Enatega-style) -------------------------------------------------
BRAND = (94, 193, 47)          # enatega green
BRAND_DK = (60, 140, 25)
BG = (245, 247, 249)
CARD = (255, 255, 255)
INK = (33, 37, 41)
MUTED = (130, 138, 146)
LINE = (223, 227, 231)
RED = (220, 53, 69)
AMBER = (255, 179, 0)
STATUS = (20, 24, 28)

W, H = 380, 780                # phone canvas


def font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def base(title="9:41"):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # status bar
    d.rectangle([0, 0, W, 28], fill=STATUS)
    d.text((14, 7), title, font=font(13, True), fill="white")
    d.text((W - 60, 7), "100% ▮", font=font(12), fill="white")
    return img, d


def header(d, text, back=True):
    d.rectangle([0, 28, W, 76], fill=CARD)
    d.line([0, 76, W, 76], fill=LINE, width=1)
    if back:
        d.text((16, 44), "‹", font=font(30, True), fill=INK)
    d.text((46 if back else 16, 46), text, font=font(17, True), fill=INK)


def annot(d, x, y, text, color=RED):
    """red annotation callout with number bubble"""
    tw = d.textlength(text, font=font(12, True))
    rrect(d, [x, y, x + tw + 16, y + 22], 6, fill=color)
    d.text((x + 8, y + 4), text, font=font(12, True), fill="white")


def save(img, name):
    path = os.path.join(OUT, name)
    img.save(path)
    print("wrote", os.path.relpath(path))


# 01 — Login (email step) ------------------------------------------------------
def login_email():
    img, d = base()
    header(d, "Login", back=True)
    rrect(d, [40, 110, W - 40, 190], 12, fill=(232, 246, 224))
    d.text((150, 140), "🥗", font=font(40))
    d.text((30, 210), "What's your email?", font=font(22, True), fill=INK)
    d.text((30, 244), "Check if you have an account with us", font=font(12), fill=MUTED)
    # input
    rrect(d, [30, 290, W - 30, 336], 10, fill=CARD, outline=LINE, width=1)
    d.text((44, 305), "demo-customer@enatega.com", font=font(14), fill=INK)
    # button
    rrect(d, [30, 360, W - 30, 408], 10, fill=BRAND)
    d.text((160, 375), "Continue", font=font(15, True), fill="white")
    annot(d, 44, 262, "1  TextInput (no testID)")
    save(img, "01-login-email.png")


# 02 — Login (password step) ---------------------------------------------------
def login_password():
    img, d = base()
    header(d, "Login", back=True)
    d.text((30, 110), "Enter your password", font=font(22, True), fill=INK)
    d.text((30, 144), "This email already exists", font=font(12), fill=MUTED)
    rrect(d, [30, 190, W - 30, 236], 10, fill=CARD, outline=LINE, width=1)
    d.text((44, 205), "••••••", font=font(16), fill=INK)
    d.text((W - 58, 203), "👁", font=font(18))
    d.text((30, 250), "Forgot password?", font=font(12, True), fill=BRAND_DK)
    rrect(d, [30, 300, W - 30, 348], 10, fill=BRAND)
    d.text((172, 315), "Login", font=font(15, True), fill="white")
    annot(d, W - 150, 250, "2  eye icon inverted", color=AMBER)
    save(img, "02-login-password.png")


# 03 — Home / restaurant list --------------------------------------------------
def home():
    img, d = base()
    d.rectangle([0, 28, W, 92], fill=BRAND)
    d.text((16, 40), "Deliver to  ▾", font=font(12), fill="white")
    d.text((16, 58), "123 Demo Street", font=font(15, True), fill="white")
    rrect(d, [16, 104, W - 16, 144], 10, fill=CARD, outline=LINE, width=1)
    d.text((30, 116), "🔍  Search restaurants & dishes", font=font(13), fill=MUTED)
    # category chips
    for i, c in enumerate(["All", "Pizza", "Burger", "Sushi"]):
        x = 16 + i * 86
        rrect(d, [x, 158, x + 78, 188], 14,
              fill=BRAND if i == 0 else CARD, outline=LINE, width=1)
        d.text((x + 14, 165), c, font=font(12, True),
               fill="white" if i == 0 else INK)
    # restaurant cards
    names = [("Pizza Palace", "★ 4.6 · 25-30 min · Free delivery"),
             ("Burger Hub", "★ 4.3 · 20-25 min · $1.99 delivery"),
             ("Sushi World", "★ 4.8 · 30-40 min · $2.49 delivery")]
    y = 208
    for n, meta in names:
        rrect(d, [16, y, W - 16, y + 150], 12, fill=CARD, outline=LINE, width=1)
        rrect(d, [16, y, W - 16, y + 92], 12, fill=(230, 236, 240))
        d.text((150, y + 32), "🍽", font=font(34))
        d.text((28, y + 100), n, font=font(15, True), fill=INK)
        d.text((28, y + 124), meta, font=font(11), fill=MUTED)
        y += 166
    save(img, "03-home-restaurants.png")


# 04 — Restaurant menu ---------------------------------------------------------
def restaurant():
    img, d = base()
    d.rectangle([0, 28, W, 150], fill=(230, 236, 240))
    d.text((150, 70), "🍽", font=font(48))
    d.text((16, 38), "‹", font=font(30, True), fill=INK)
    rrect(d, [0, 150, W, H], 0, fill=BG)
    d.text((20, 164), "Pizza Palace", font=font(20, True), fill=INK)
    d.text((20, 194), "★ 4.6 (1.2k) · 25-30 min · Free delivery", font=font(11), fill=MUTED)
    d.text((20, 226), "Popular", font=font(15, True), fill=INK)
    items = [("Margherita Pizza", "$8.50"), ("Pepperoni Pizza", "$10.00"),
             ("Veggie Supreme", "$9.25")]
    y = 252
    for n, p in items:
        rrect(d, [16, y, W - 16, y + 84], 12, fill=CARD, outline=LINE, width=1)
        rrect(d, [24, y + 12, 84, y + 72], 8, fill=(230, 236, 240))
        d.text((40, y + 30), "🍕", font=font(22))
        d.text((100, y + 16), n, font=font(14, True), fill=INK)
        d.text((100, y + 44), p, font=font(13), fill=BRAND_DK)
        rrect(d, [W - 66, y + 26, W - 26, y + 60], 8, fill=BRAND)
        d.text((W - 52, y + 33), "+", font=font(18, True), fill="white")
        y += 98
    save(img, "04-restaurant-menu.png")


# 05 — Item detail with Add to Cart -------------------------------------------
def item_detail():
    img, d = base()
    d.rectangle([0, 28, W, 210], fill=(230, 236, 240))
    d.text((165, 100), "🍕", font=font(56))
    d.text((16, 40), "‹", font=font(30, True), fill=INK)
    d.text((20, 226), "Margherita Pizza", font=font(20, True), fill=INK)
    d.text((20, 256), "$8.50", font=font(16, True), fill=BRAND_DK)
    d.text((20, 286), "Classic tomato, mozzarella & basil.", font=font(12), fill=MUTED)
    # qty stepper
    d.text((20, 330), "Quantity", font=font(14, True), fill=INK)
    rrect(d, [W - 150, 322, W - 20, 360], 10, fill=CARD, outline=LINE, width=1)
    d.text((W - 138, 330), "–", font=font(20, True), fill=INK)
    d.text((W - 90, 330), "1", font=font(16, True), fill=INK)
    d.text((W - 44, 330), "+", font=font(20, True), fill=BRAND_DK)
    # add to cart
    rrect(d, [20, H - 70, W - 20, H - 22], 12, fill=BRAND)
    d.text((105, H - 56), "Add to Cart · $8.50", font=font(15, True), fill="white")
    annot(d, 40, H - 104, "Add to Cart CTA")
    save(img, "05-item-detail.png")


# 06 — Cart --------------------------------------------------------------------
def cart(empty=False):
    img, d = base()
    header(d, "Your Cart", back=True)
    if empty:
        d.text((150, 300), "🛒", font=font(52))
        d.text((110, 380), "Your cart is empty", font=font(15, True), fill=MUTED)
        save(img, "06-cart-empty.png")
        return
    y = 96
    for n, p, q in [("Margherita Pizza", "$8.50", "2"), ("Pepperoni Pizza", "$10.00", "1")]:
        rrect(d, [16, y, W - 16, y + 84], 12, fill=CARD, outline=LINE, width=1)
        rrect(d, [24, y + 12, 84, y + 72], 8, fill=(230, 236, 240))
        d.text((44, y + 30), "🍕", font=font(22))
        d.text((100, y + 16), n, font=font(14, True), fill=INK)
        d.text((100, y + 44), p, font=font(13), fill=BRAND_DK)
        rrect(d, [W - 116, y + 26, W - 24, y + 62], 8, fill=BG, outline=LINE, width=1)
        d.text((W - 104, y + 34), "–", font=font(16, True), fill=INK)
        d.text((W - 72, y + 34), q, font=font(14, True), fill=INK)
        d.text((W - 44, y + 34), "+", font=font(16, True), fill=BRAND_DK)
        y += 98
    # summary
    rrect(d, [16, y + 6, W - 16, y + 120], 12, fill=CARD, outline=LINE, width=1)
    d.text((30, y + 20), "Subtotal", font=font(12), fill=MUTED)
    d.text((W - 80, y + 20), "$27.00", font=font(12, True), fill=INK)
    d.text((30, y + 46), "Delivery", font=font(12), fill=MUTED)
    d.text((W - 80, y + 46), "$1.99", font=font(12, True), fill=INK)
    d.text((30, y + 78), "Total", font=font(14, True), fill=INK)
    d.text((W - 90, y + 78), "$28.99", font=font(14, True), fill=BRAND_DK)
    rrect(d, [20, H - 66, W - 20, H - 20], 12, fill=BRAND)
    d.text((120, H - 52), "Checkout", font=font(15, True), fill="white")
    annot(d, W - 150, 60, "3  qty stepper")
    save(img, "06-cart.png")


# 07 — Checkout ----------------------------------------------------------------
def checkout():
    img, d = base()
    header(d, "Checkout", back=True)
    d.text((20, 96), "Delivery address", font=font(14, True), fill=INK)
    rrect(d, [16, 122, W - 16, 168], 10, fill=CARD, outline=LINE, width=1)
    d.text((30, 136), "📍  123 Demo Street, Apt 4", font=font(12), fill=INK)
    d.text((20, 190), "Payment method", font=font(14, True), fill=INK)
    rrect(d, [16, 216, W - 16, 262], 10, fill=CARD, outline=LINE, width=1)
    d.text((30, 230), "💵  Cash on delivery", font=font(12), fill=INK)
    d.text((20, 288), "Order summary", font=font(14, True), fill=INK)
    rrect(d, [16, 314, W - 16, 420], 10, fill=CARD, outline=LINE, width=1)
    d.text((30, 328), "2 × Margherita Pizza", font=font(12), fill=INK)
    d.text((W - 80, 328), "$17.00", font=font(12, True), fill=INK)
    d.text((30, 356), "1 × Pepperoni Pizza", font=font(12), fill=INK)
    d.text((W - 80, 356), "$10.00", font=font(12, True), fill=INK)
    d.line([30, 384, W - 30, 384], fill=LINE)
    d.text((30, 392), "Total", font=font(13, True), fill=INK)
    d.text((W - 90, 392), "$28.99", font=font(13, True), fill=BRAND_DK)
    rrect(d, [20, H - 66, W - 20, H - 20], 12, fill=BRAND)
    d.text((110, H - 52), "Place Order", font=font(15, True), fill="white")
    save(img, "07-checkout.png")


# BUG-01 — email regex rejects valid TLD ---------------------------------------
def bug_email():
    img, d = base()
    header(d, "Login", back=True)
    d.text((30, 110), "What's your email?", font=font(22, True), fill=INK)
    rrect(d, [30, 170, W - 30, 216], 10, fill=CARD, outline=RED, width=2)
    d.text((44, 185), "user@company.store", font=font(14), fill=INK)
    d.text((30, 226), "⚠ Please enter a valid email", font=font(12, True), fill=RED)
    rrect(d, [30, 260, W - 30, 308], 10, fill=(200, 210, 216))
    d.text((150, 275), "Continue", font=font(15, True), fill="white")
    annot(d, 30, 330, "BUG-001  valid .store TLD rejected")
    save(img, "bug-01-email-regex.png")


# BUG-02 — no testID (inspector view) ------------------------------------------
def bug_testid():
    img, d = base()
    header(d, "UI Automator dump", back=False)
    d.text((16, 96), "<android.widget.EditText", font=font(12, True), fill=INK)
    d.text((28, 118), 'resource-id=""', font=font(12), fill=RED)
    d.text((28, 140), 'content-desc=""', font=font(12), fill=RED)
    d.text((28, 162), 'text="" hint="Email" />', font=font(12), fill=MUTED)
    d.text((16, 196), "<android.widget.EditText", font=font(12, True), fill=INK)
    d.text((28, 218), 'resource-id=""', font=font(12), fill=RED)
    d.text((28, 240), 'content-desc="" />', font=font(12), fill=RED)
    annot(d, 16, 280, "BUG-002  no resource-id / content-desc")
    d.text((16, 320), "=> only absolute XPath locators possible", font=font(11), fill=MUTED)
    save(img, "bug-02-no-testid.png")


if __name__ == "__main__":
    login_email(); login_password(); home(); restaurant()
    item_detail(); cart(False); cart(True); checkout()
    bug_email(); bug_testid()
    print("done")
