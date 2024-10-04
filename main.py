from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notifypy import Notify
from bs4 import BeautifulSoup
from datetime import datetime
from pymongo import MongoClient
import os
import sys

client = MongoClient("mongodb://localhost:27017/")
db = client["amazon"]
collection = db["prices"]


def get_data():
    
    options = Options()
    
    options.add_argument("--headless")
    # options.add_argument("--proxy-server = gate.nodemaven.com:8080")

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    
    with open("products.txt") as f:
        products = f.readlines()
        

    driver = webdriver.Chrome(options=options)

    for product in products:
        driver.get(f"https://www.amazon.in/dp/{product}")
        page_source = driver.page_source
        with open(f"data/{product.strip()}.html", "w", encoding="utf-8") as f:
            f.write(page_source)
        
def extract_data():
    files = os.listdir("data")
    for file in files:
        print(file)
        with open(f"data/{file}", encoding="utf-8") as f:
            content = f.read()
            
        soup = BeautifulSoup(content, 'html.parser')
        Title = soup.title.getText().split(":")[0]
        Time = datetime.now()
        price = soup.find(class_="a-price-whole")
        priceINT = price.getText().replace(".","").replace(",","")
        table = soup.find(id="productDetails_detailBullets_sections1")
        ASIN = table.find(class_="a-size-base prodDetAttrValue").getText().strip()
        print(Title, priceINT, ASIN, Time)
        collection.insert_one({"Title":Title, "priceINT": priceINT, "ASIN":ASIN, "Time":Time})
        # with open("FinalData.txt", "a") as f:
            # f.write(f"{Title}~~{priceINT}~~{ASIN}~~{Time}\n")
            
if __name__ == "__main__":
    get_data()
    extract_data()
    


