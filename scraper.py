import requests
from bs4 import BeautifulSoup


product_code = '95319759'
url = f'https://www.ceneo.pl/{product_code}#tab=reviews'
response = requests.get(url)
page_dom = BeautifulSoup(response.text, 'html.parser')
opinions = page_dom.select('div.js_product-review')
for opinion in opinions:
    print(opinion['data-entry-id'])
print(type(page_dom))
print(type(opinions))
print(len(opinions))