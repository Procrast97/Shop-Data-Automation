import os
os.environ.setdefault('FLASK_KEY', 'demo-seed-key')

from app import app
from DBModels import db, Users, Urls, Shops, ShopLoc, ItemData
from werkzeug.security import generate_password_hash

DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "Demo1234!"
DEMO_USERNAME = "demo"


def seed():
    with app.app_context():
        db.create_all()

        if db.session.execute(db.select(Users).where(Users.email == DEMO_EMAIL)).scalar():
            print("Demo data already exists. Skipping.")
            return

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

        items = [
            # --- 01/05/2026 ---
            ItemData(date="01/05/2026", shop_name="Central (VD)",      customer="John Smith",   description="iPhone 15 Case",       product_id="C001", qty=2, price="$ 25",  subtotal="$ 50",  loc_id=central.id),
            ItemData(date="01/05/2026", shop_name="Central (VD)",      customer="Mary Johnson", description="Screen Protector",      product_id="C002", qty=3, price="$ 15",  subtotal="$ 45",  loc_id=central.id),
            ItemData(date="01/05/2026", shop_name="Causeway Bay (VD)", customer="David Lee",    description="Wireless Charger",      product_id="C003", qty=1, price="$ 80",  subtotal="$ 80",  loc_id=causeway.id),
            # --- 08/05/2026 ---
            ItemData(date="08/05/2026", shop_name="Causeway Bay (VD)", customer="Sarah Wong",   description="USB-C Cable",           product_id="C004", qty=2, price="$ 20",  subtotal="$ 40",  loc_id=causeway.id),
            ItemData(date="08/05/2026", shop_name="Mong Kok (VD)",     customer="Peter Chan",   description="Power Bank",            product_id="C005", qty=1, price="$ 120", subtotal="$ 120", loc_id=mongkok.id),
            ItemData(date="08/05/2026", shop_name="Mong Kok (VD)",     customer="Lisa Ng",      description="Bluetooth Earphones",   product_id="C006", qty=1, price="$ 200", subtotal="$ 200", loc_id=mongkok.id),
            # --- 15/05/2026 ---
            ItemData(date="15/05/2026", shop_name="Central (VD)",      customer="Tom Brown",    description="Phone Stand",           product_id="C007", qty=2, price="$ 35",  subtotal="$ 70",  loc_id=central.id),
            ItemData(date="15/05/2026", shop_name="Central (VD)",      customer="Amy Chen",     description="Laptop Sleeve",         product_id="C008", qty=1, price="$ 65",  subtotal="$ 65",  loc_id=central.id),
            ItemData(date="15/05/2026", shop_name="Causeway Bay (VD)", customer="Kevin Ho",     description="Smart Watch Band",      product_id="C009", qty=3, price="$ 30",  subtotal="$ 90",  loc_id=causeway.id),
            # --- 22/05/2026 ---
            ItemData(date="22/05/2026", shop_name="Mong Kok (VD)",     customer="Rachel Lam",   description="Portable Speaker",      product_id="C010", qty=1, price="$ 150", subtotal="$ 150", loc_id=mongkok.id),
            ItemData(date="22/05/2026", shop_name="Mong Kok (VD)",     customer="Michael Yip",  description="Keyboard Cover",        product_id="C011", qty=2, price="$ 45",  subtotal="$ 90",  loc_id=mongkok.id),
            ItemData(date="22/05/2026", shop_name="Central (VD)",      customer="Emily Tsang",  description="AirPods Case",          product_id="C012", qty=1, price="$ 55",  subtotal="$ 55",  loc_id=central.id),
            # --- 29/05/2026 ---
            ItemData(date="29/05/2026", shop_name="Causeway Bay (VD)", customer="James Liu",    description="Camera Lens Filter",    product_id="C013", qty=2, price="$ 75",  subtotal="$ 150", loc_id=causeway.id),
            ItemData(date="29/05/2026", shop_name="Causeway Bay (VD)", customer="Grace Fung",   description="Laptop Stand",          product_id="C014", qty=1, price="$ 180", subtotal="$ 180", loc_id=causeway.id),
            ItemData(date="29/05/2026", shop_name="Mong Kok (VD)",     customer="Victor Ma",    description="Tablet Cover",          product_id="C015", qty=2, price="$ 60",  subtotal="$ 120", loc_id=mongkok.id),
        ]
        db.session.add_all(items)
        db.session.commit()

        print("Demo data seeded successfully!")
        print(f"  User:      {DEMO_EMAIL} / {DEMO_PASSWORD}")
        print(f"  Shop:      VD (Vector Digital)")
        print(f"  Locations: Central, Causeway Bay, Mong Kok")
        print(f"  Items:     15 across 5 days in May 2026")
        print()
        print("To view all demo items in Reports, use:")
        print("  Custom Date Range  ->  From: 2026-05-01  /  To: 2026-05-31")


if __name__ == "__main__":
    seed()