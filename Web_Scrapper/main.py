from bs4 import BeautifulSoup
import requests
import pandas as pd

item = input("Enter the item you want to search for on Amazon and Flipkart: ")

amazon_url = f"https://www.amazon.in/s?k={item}"
flipkart_url = f"https://www.flipkart.com/search?q={item}"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}

amazon = {'Title': [], 'Price': []}
flipkart = {'Title': [], 'Price': []}

# Amazon scraping
req_amazon = requests.get(amazon_url, headers=headers)
soup_amazon = BeautifulSoup(req_amazon.text, 'html.parser')

amazon_product_containers = soup_amazon.select("div.s-main-slot div.s-result-item")

for container in amazon_product_containers:
    name_tag = container.select_one("span.a-size-medium.a-color-base.a-text-normal")
    price_tag = container.select_one("span.a-price > span.a-offscreen")

    if name_tag and price_tag:
        print(f"Amazon Product: {name_tag.get_text(strip=True)}")
        print(f"Amazon Price: {price_tag.get_text(strip=True)}")
        amazon["Title"].append(name_tag.get_text(strip=True))
        amazon["Price"].append(price_tag.get_text(strip=True))

# Flipkart scraping
req_flipkart = requests.get(flipkart_url, headers=headers)
soup_flipkart = BeautifulSoup(req_flipkart.text, 'html.parser')

flipkart_product_containers = soup_flipkart.find_all("div._75nlfW")

for container in flipkart_product_containers:
    name_tag = container.select_one("div.KzDlHZ")
    price_tag = container.select_one("div.Nx9bqj._4b5DiR")

    if name_tag and price_tag:
        print(f"Flipkart Product: {name_tag.get_text(strip=True)}")
        print(f"Flipkart Price: {price_tag.get_text(strip=True)}")
        flipkart["Title"].append(name_tag.get_text(strip=True))
        flipkart["Price"].append(price_tag.get_text(strip=True))

df_amazon = pd.DataFrame.from_dict(amazon)
df_amazon.to_csv("amazon.csv", index=False)

df_flipkart = pd.DataFrame.from_dict(flipkart)
df_flipkart.to_csv("flipkart.csv", index=False)