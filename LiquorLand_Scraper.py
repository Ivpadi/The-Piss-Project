from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import date, datetime
from extraction_methods import get_container, get_size, get_ml


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:152.0) Gecko/20100101 Firefox/152.0"
}

BASE_URL = "https://www.liquorland.co.nz/beer"



def get_products():

    page = 1

    all_products = []

    while True:

        url = f"{BASE_URL}?p={page}&s%5Brelevance%5D=desc"

        html = requests.get(url, headers=HEADERS)

        soup = BeautifulSoup(html.text, 'html.parser')

        script_tag = soup.find('script', string= lambda s: s and 'window.category' in s)


        if not script_tag:
            print("No products found")
            break

        raw_text = script_tag.text

        start = raw_text.find("...{") + 3

        brace_count = 0
        end = None

        # iterate through text to find final matching brace
        for i in range(start, len(raw_text)):

            if raw_text[i] == "{":
                brace_count+= 1

            elif raw_text[i] == "}":
                brace_count-= 1

                if brace_count == 0:
                    end = i
                    break


        # extract and store pure json
        json_text = raw_text[start:end + 1]

        data = json.loads(json_text)

        products = data["items"]

        if not products:
            break

        all_products.extend(products)

        #print(f"Page {page}: {len(products)}")

        if len(products) == 0:
            break

        page += 1


        #for prod in all_products:
           # print(prod["description"])

    return all_products


def get_abv(product_url):

    html = requests.get(product_url, headers=HEADERS)

    soup = BeautifulSoup(html.text, 'html.parser')

    meta_tag = soup.find("meta", attrs={'name':'description'})

    content = meta_tag.get('content')

    abv_check = re.compile(r"\d.\d%")

    abv = re.search(abv_check, content)
    
    if abv:
        return abv.group(0)

    else:
        return "Not Available"


test_url = "https://www.liquorland.co.nz/export-gold-24-pack-bottles-330ml-9414339823338"
test = get_abv(test_url)

print(test)


def clean_products(all_products):

    all_cleaned_products = []

    for prod in all_products:

        cleaned_product = {}

        cleaned_product["raw_name"] = prod["description"]
        cleaned_product["product_url"] = "https://www.liquorland.co.nz/" + prod["stylecolour"]["urlkey"]
        cleaned_product["image_url"] = prod["stylecolour"]["primaryimage"]["src"]
        cleaned_product["last_seen"] = date.today()
        cleaned_product["brand"] = prod["label"]
        cleaned_product["category"] = prod["department"]
        cleaned_product["container_type"] = get_container(prod["description"])
        cleaned_product["pack_size"] = get_size(prod["description"])
        cleaned_product["volume_ml"] = get_ml(prod["description"])
        cleaned_product["abv"] = get_abv(cleaned_product["product_url"])
        cleaned_product["standard_drinks"] = get_standards()
        cleaned_product["price"] = prod["stylecolour"]["variants"][0]["unitprice"]
        cleaned_product["scraped_at"] = datetime.now()

        all_cleaned_products.append(cleaned_product)

    return all_cleaned_products