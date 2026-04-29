from selenium import webdriver
from selenium.common import StaleElementReferenceException, WebDriverException
from selenium.webdriver.ie.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime as dt
from urllib3.exceptions import MaxRetryError
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
import time
import smtplib
from email.message import EmailMessage

# Used to load the environmental variables:
load_dotenv()

EMAIL = os.environ.get('ACCOUNT_EMAIL')
PASSWORD = os.environ.get('ACCOUNT_PASSWORD')
MAX_ATTEMPTS = 3
DELAY = 2
DEFAULT_RETURN = "Failed"
SEND_EMAIL = os.environ.get('SEND_EMAIL')
SEND_PASSWORD = os.environ.get('SEND_PASSWORD')
# connection = smtplib.SMTP_SSL("smtp.gmail.com")

def error_control(max_attempts, delay, default_return):
    def decorator(func):
        def manager(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        print({args[1] if len(args) > 1 else 'unknown'})
                    #     connection.sendmail(
                    #     from_addr=SEND_EMAIL,
                    #     to_addrs="zanderhenning@gmail.com",
                    #     msg=f"Subject: VincentStockApp - Error\n\nError with shop {args[1] if len(args) > 1 else 'unknown'}. Element not found."
                    # )
                        # connection.login(SEND_EMAIL, SEND_PASSWORD)
                        # connection.sendmail(from_addr=SEND_EMAIL, to_addrs="zanderhenning@gmail.com",
                        #                          msg=f"Subject: VincentStockApp - Error occured\n\nThe following error '{e}' occured with shop {args[1] if len(args) > 1 else 'unknown'}.")
                        return default_return
                    time.sleep(delay)
            return default_return

        return manager

    return decorator

class DataExtraction:

    def __init__(self):
        from selenium.webdriver.chrome.service import Service

        self.chrome_options = Options()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--headless=new')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        service = Service(executable_path='/usr/bin/chromedriver')
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 5)


    # @error_control(max_attempts=MAX_ATTEMPTS, delay=DELAY, default_return=DEFAULT_RETURN)
    def get_website(self, url):

        try:
            # print("Getting website...")
            self.driver.get(url)
            time.sleep(2)
            # print("Done")
        except MaxRetryError:
            self.driver.quit()
            self.driver.get(url)
            time.sleep(2)

        # Input Login Details:
        email = self.wait.until(ec.presence_of_element_located((By.NAME, "vendor_email")))
        email.send_keys(EMAIL)
        password = self.wait.until(ec.presence_of_element_located((By.NAME, "vendor_password")))
        password.send_keys(PASSWORD)

        # Enter pressing:
        submit_login = self.driver.find_element(By.NAME, "Submit")
        submit_login.click()

        try:
            ## After login, enter sales and generate day sales:
            nav_to_sales = self.wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/table[1]/tbody/tr[2]/td/a[1]")))
            nav_to_sales.click()
        except Exception as e:
            # print(f"Element 'sales' has not loaded yet, error: {e}.\nTrying again...")
            nav_to_sales = self.wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/table[1]/tbody/tr[2]/td/a[1]")))
            nav_to_sales.click()

        ##Testing Purposes:
        # date = self.wait.until(ec.presence_of_element_located((By.XPATH, "/html/body/table[2]/tbody/tr[7]/td[3]/select[3]/option[3]")))
        # date.click()

    # @error_control(max_attempts=MAX_ATTEMPTS, delay=DELAY, default_return=DEFAULT_RETURN)
    def open_shops(self, shop_loc):
        shop_dd = self.driver.find_element(By.XPATH, "/html/body/table[2]/tbody/tr[6]/td[3]/select")
        shop_dd.click()
        shop_name = shop_loc.split(" ")[0]
        shop_selector = self.driver.find_element(By.XPATH, f"/html/body/table[2]/tbody/tr[6]/td[3]/select/option[contains(text(), '{shop_name}')]")
        shop_selector.click()

        # Submit request:
        submit_year_data = self.driver.find_element(By.NAME, "submit")
        submit_year_data.click()


        return self.scrape_data(shop_loc)

    # @error_control(max_attempts=MAX_ATTEMPTS, delay=DELAY, default_return=DEFAULT_RETURN)
    def scrape_data(self, current_loc):
        ## Now time to scrape the data:
        all_data = []

        """THere was an error that kept happening in no specific shop at a time where the last two (empty and total) tr 
        elements where included in the data extraction and would cause an error during dictionary formating. This 'time.sleep(1)'
        was inserted to help give the template and it's elements time to stabilise before performing the action."""
        time.sleep(1)

        data_length = len(self.driver.find_elements(By.XPATH, value=f"/html/body/table[2]/tbody/tr[9]/td/table/tbody/tr"))

        for num in range(3, data_length - 1):
            tr_data = self.driver.find_elements(By.XPATH, value=f"/html/body/table[2]/tbody/tr[9]/td/table/tbody/tr[{num}]/td")
            td_data_list = [item.text for item in tr_data]
            td_data_list = [item for item in td_data_list if item.strip()]
            if len(td_data_list) == 0:
                pass
            else:
                td_data_list.insert(1, current_loc)
                all_data.append(td_data_list)
        return all_data


    def create_dict(self, accu_data):
        headings_list = ["Date", "Shop name", "Customer", "Description", "Product ID", "Qty", "Price", "Sub."]

        ## Add data to workable dictionary:
        # Debug: Check if all rows have the same length
        # for idx, row in enumerate(accu_data):
        #     if len(row) != len(headings_list):
        #         print(f"Row {idx} has {len(row)} elements, expected {len(headings_list)}")
        #         print(f"Row content: {row}")
        #         print(f"Headers: {headings_list}")

        data = {f"{accu_data.index(i)}": {head: i[headings_list.index(head)] for head in headings_list} for i in accu_data}
        # print(data)

        ## Formate date from MM/DD/YYYY to DD/MM/YYYY:
        for item in range(0, len(accu_data)):
            # print(item)
            date_strip = dt.strptime(data[f"{item}"]["Date"].split(" ")[0], "%m/%d/%Y")
            formated_date = date_strip.strftime("%d/%m/%Y")
            data[f"{item}"]["Date"] = formated_date

        return data


    def log_out(self):
        xpath = "/html/body/table[1]/tbody/tr[2]/td/a[6]"
        for attempts in range(3):
            try:
                time.sleep(1)
                self.driver.execute_script("""
                                var element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                                if (element) element.click();
                            """, xpath)
                break
            except (StaleElementReferenceException, WebDriverException) as e:
                if attempts == 2:
                    return "The program crashed due to a StaleElementReferenceException during logout."
                time.sleep(1)


    def quit(self):
        self.driver.quit()


