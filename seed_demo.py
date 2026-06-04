import os
import sys
import random

os.environ.setdefault('FLASK_KEY', 'demo-seed-key')

from app import app
from DBModels import db, Users, Urls, Shops, ShopLoc, ItemData
from werkzeug.security import generate_password_hash

DEMO_EMAIL    = "demo@example.com"
DEMO_PASSWORD = "Demo1234!"
DEMO_USERNAME = "demo"

CUSTOMERS = [
    "John Smith",    "Mary Johnson",  "David Lee",     "Sarah Wong",    "Peter Chan",
    "Lisa Ng",       "Tom Brown",     "Amy Chen",      "Kevin Ho",      "Rachel Lam",
    "Michael Yip",   "Emily Tsang",   "James Liu",     "Grace Fung",    "Victor Ma",
    "Alice Chan",    "Bob Wong",      "Carol Ng",      "Daniel Ho",     "Eva Lam",
    "Frank Tsui",    "Gary Cheng",    "Helen Yau",     "Ivan Mak",      "Jenny Lo",
    "Kenneth Pang",  "Linda Kwok",    "Martin Fok",    "Nancy Au",      "Oscar Tong",
    "Pamela Wu",     "Quinn Sze",     "Roger Hui",     "Stella Lau",    "Terry Yu",
    "Uma Kwan",      "Vincent Siu",   "Wendy Tam",     "Xavier Yuen",   "Yvonne Ko",
]

PRODUCTS = [
    ("iPhone 15 Case",       25),
    ("Screen Protector",     15),
    ("Wireless Charger",     80),
    ("USB-C Cable",          20),
    ("Power Bank",          120),
    ("Bluetooth Earphones", 200),
    ("Phone Stand",          35),
    ("Laptop Sleeve",        65),
    ("Smart Watch Band",     30),
    ("Portable Speaker",    150),
    ("Keyboard Cover",       45),
    ("AirPods Case",         55),
    ("Camera Lens Filter",   75),
    ("Laptop Stand",        180),
    ("Tablet Cover",         60),
    ("iPad Stand",           40),
    ("Car Mount",            25),
    ("Screen Cleaning Kit",  10),
    ("Memory Card 128GB",    55),
    ("Cable Organizer",      18),
    ("Pop Socket",           15),
    ("USB Hub 4-Port",       45),
    ("HDMI Adapter",         35),
    ("SD Card Reader",       28),
    ("Stylus Pen",           40),
    ("Wireless Mouse",       88),
    ("Mini Tripod",          38),
    ("Magnetic Phone Mount", 32),
    ("LED Desk Light",       95),
    ("Smart Plug",           55),
]


def seed(force=False):
    with app.app_context():
        db.create_all()

        existing = db.session.execute(
            db.select(Users).where(Users.email == DEMO_EMAIL)
        ).scalar()

        if existing:
            if not force:
                print("Demo data already exists. Run with --force to re-seed.")
                return
            db.session.delete(existing)
            db.session.commit()
            print("Removed existing demo data.")

        user = Users(
            username=DEMO_USERNAME,
            email=DEMO_EMAIL,
            password=generate_password_hash(DEMO_PASSWORD, method='pbkdf2:sha256', salt_length=8),
        )
        db.session.add(user)
        db.session.flush()

        url = Urls(url_address="https://www.one-pos.com/vectordigital/box_login.asp", user_id=user.id)
        db.session.add(url)
        db.session.flush()

        shop = Shops(shop_name="VD", url_id=url.id)
        db.session.add(shop)
        db.session.flush()

        central  = ShopLoc(shop_loc="Central",      shop_id=shop.id)
        causeway = ShopLoc(shop_loc="Causeway Bay", shop_id=shop.id)
        mongkok  = ShopLoc(shop_loc="Mong Kok",     shop_id=shop.id)
        db.session.add_all([central, causeway, mongkok])
        db.session.flush()

        locs = [
            (central,  "Central (VD)"),
            (causeway, "Causeway Bay (VD)"),
            (mongkok,  "Mong Kok (VD)"),
        ]

        rng = random.Random(42)
        items = []
        pid = 1

        for day in range(1, 32):
            date_str = f"{day:02d}/05/2026"
            n = rng.randint(5, 10)
            for _ in range(n):
                loc_obj, loc_name = rng.choice(locs)
                customer         = rng.choice(CUSTOMERS)
                desc, unit_price = rng.choice(PRODUCTS)
                qty              = rng.randint(1, 3)
                subtotal         = unit_price * qty
                items.append(ItemData(
                    date=date_str,
                    shop_name=loc_name,
                    customer=customer,
                    description=desc,
                    product_id=f"C{pid:03d}",
                    qty=qty,
                    price=f"$ {unit_price}",
                    subtotal=f"$ {subtotal}",
                    loc_id=loc_obj.id,
                ))
                pid += 1

        db.session.add_all(items)
        db.session.commit()

        print("Demo data seeded successfully!")
        print(f"  User:      {DEMO_EMAIL} / {DEMO_PASSWORD}")
        print(f"  Shop:      VD (Vector Digital)")
        print(f"  Locations: Central, Causeway Bay, Mong Kok")
        print(f"  Items:     {len(items)} across all 31 days in May 2026")
        print()
        print("To view all demo items in Reports, use:")
        print("  Custom Date Range  ->  From: 01/05/2026  /  To: 31/05/2026")


if __name__ == "__main__":
    force = "--force" in sys.argv or "-f" in sys.argv
    seed(force=force)
