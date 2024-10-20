import re
import requests
import pandas as pd

from bs4 import BeautifulSoup


# traverse each sub-category and fetch all the product's price, name, and images
noisy_str = re.compile("[^\d\.]")

product_info = []
uri_response = requests.get(url='https://mymall.se/sport-fritid/outdoor/kompasser').content
bs_obj = BeautifulSoup(markup=uri_response, parser='html.parser', features='lxml')

unordered_product = bs_obj.select('div.product-item')
for unordered_products in unordered_product:
    if hasattr(unordered_products, 'contents'):
        try:
            product_info.append({
                'product_name': unordered_products.contents[1].text.strip(),
                'product_price': float(noisy_str.sub(r'', unordered_products.contents[2].text)),
                'image_url': unordered_products.contents[0].find('a', href=True).get('href'),
                'sub_category_url': 'https://mymall.se/sport-fritid/outdoor/kompasser'
            })
        except (IndexError, ValueError):
            pass

# add data into panda dataframe
prod_df = pd.DataFrame(data=product_info, columns=['product_name', 'product_price', 'image_url', 'sub_category_url'])
