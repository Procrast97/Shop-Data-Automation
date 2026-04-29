import time
import schedule
from datetime import datetime as dt
from DBModels import db, Urls, Shops, ShopLoc, ItemData
from DataExtract import DataExtraction
from ExcelFormatting import ExcelCreation
from main import app
import os

from dotenv import load_dotenv
load_dotenv()

EMAIL = os.environ.get('SYSTEM_EMAIL')
PASSWORD = os.environ.get('SYSTEM_PASSWORD')
ALL_DATA = []
TOTAL_SALES = []
EMPTY_STORES = []
SALES_SHOPS = []


def task():
    with app.app_context():
        try:
            utc_time = dt.utcnow()
            cutoff = utc_time.replace(hour=14, minute=00, second=0, microsecond=0)

            get_data = DataExtraction()
            excel = ExcelCreation()

            # Extract the list of existing URLs currently in the database:
            url_list = db.session.execute(db.select(Urls.url_address)).scalars().all()

            for url in url_list:
                get_data.get_website(url)
                # Obtain the url instance from Urls database:
                current_url = db.session.execute(db.select(Urls).where(Urls.url_address == url)).scalar()

                # Get the current shop abbr to append to the shop_loc name to add to the database for later use:
                current_name_item = db.session.execute(db.select(Shops).where(Shops.url_id == current_url.id)).scalar()
                if not current_name_item:
                    print(f"ERROR: No shop found for URL: {url}, url_id: {current_url.id}")
                    continue
                current_abbr = current_name_item.shop_name

                for loc in db.session.execute(db.select(ShopLoc).where(ShopLoc.shop_id == current_url.id)).scalars().all():
                    shop_loc = loc.shop_loc
                    print(shop_loc)
                    added_abbr = f"{shop_loc} ({current_abbr})"
                    current_data = get_data.open_shops(added_abbr)
                    if len(current_data) == 0:
                        print(added_abbr)
                        EMPTY_STORES.append(added_abbr)
                    else:
                        print(added_abbr)
                        SALES_SHOPS.append(added_abbr)
                        for item in current_data:
                            ALL_DATA.append(item)
                print(ALL_DATA)
                get_data.log_out()
                time.sleep(2)

            dict_data = get_data.create_dict(ALL_DATA)
            for sub in range(0, len(dict_data)):
                TOTAL_SALES.append(float(dict_data[f"{sub}"]["Sub."].split(" ")[1]))

            form_data = excel.create_excelsheet(dict_data)
            form_populated = True

            if form_data.empty:
                form_populated = False
                remove_columns = []
            else:
                remove_columns = excel.removing_columns(form_data)
                excel.create_pdf(form_data)

            excel.send_mail(email=EMAIL, password=PASSWORD, empty_shop_list=EMPTY_STORES,
                          sales_shops_list=SALES_SHOPS, total=sum(TOTAL_SALES),
                          r_data=remove_columns, send_condition=form_populated)

            if utc_time >= cutoff:
                for num in range(len(dict_data)):
                    try:
                        item = dict_data[f"{num}"]
                        shop_name = item["Shop name"].split(" ")
                        if len(shop_name) < 2:
                            print(f"Invalid Shop Name. Shop Name: {shop_name}")
                            continue

                        current_loc = shop_name[0]
                        current_abbr = shop_name[-1].replace("(", "").replace(")", "")

                        get_shop_abbr = db.session.execute(
                            db.select(Shops).where(Shops.shop_name == current_abbr)
                        ).scalar()

                        if not get_shop_abbr:
                            print(f"The shop abbreviation {current_abbr} does not exist in the database.")
                            continue

                        get_loc = db.session.execute(
                            db.select(ShopLoc).where(
                                ShopLoc.shop_loc == current_loc,
                                ShopLoc.shop_id == get_shop_abbr.id
                            )
                        ).scalar()

                        if not get_loc:
                            print(f"The shop location {current_loc} does not exist in the database.")
                            continue

                        existing_item = db.session.execute(
                            db.select(ItemData).where(
                                ItemData.date == dict_data[f"{num}"]["Date"],
                                ItemData.product_id == dict_data[f"{num}"]["Product ID"],
                                ItemData.customer == dict_data[f"{num}"]["Customer"],
                            )
                        ).scalar_one_or_none()

                        if not existing_item:
                            new_item = ItemData(
                                date=dict_data[f"{num}"]["Date"],
                                shop_name=dict_data[f"{num}"]["Shop name"],
                                customer=dict_data[f"{num}"]["Customer"],
                                description=dict_data[f"{num}"]["Description"],
                                product_id=dict_data[f"{num}"]["Product ID"],
                                qty=dict_data[f"{num}"]["Qty"],
                                price=dict_data[f"{num}"]["Price"],
                                subtotal=dict_data[f"{num}"]["Sub."],
                                loc_id=get_loc.id,
                            )
                            db.session.add(new_item)

                    except Exception as e:
                        print(f"Error processing item {num}: {e}")
                        continue

                db.session.commit()
                print(f"Task completed successfully at {dt.now()}")

        except Exception as e:
            import traceback
            print(f"Error processing automation: {e}")
            print("Full traceback:")
            traceback.print_exc()

        finally:
            EMPTY_STORES.clear()
            SALES_SHOPS.clear()
            ALL_DATA.clear()
            TOTAL_SALES.clear()
            try:
                get_data.quit()
            except:
                pass


schedule.every().day.at("09:00").do(task)
schedule.every().day.at("14:00").do(task)

if __name__ == "__main__":
    print(f"Scheduler started at {dt.now()}")
    print("Scheduled tasks: 09:00 UTC and 14:00 UTC daily")
    while True:
        schedule.run_pending()
        time.sleep(60)
