import re
import requests
import pandas as pd

from bs4 import BeautifulSoup


MENU_URI = "https://mymall.se/media/mymall/megamenu/9826648.html"

data = []
uri_response = requests.get(url=MENU_URI).content
bs_obj = BeautifulSoup(markup=uri_response, parser='html.parser', features='lxml')

unordered_li = bs_obj.select('body > li')

for un_lis in unordered_li:
    # get the mega category info first
    mega_cat_name = un_lis.contents[1].text.strip()
    mega_cat_uri = un_lis.contents[1].find('a', href=True).get('href')

    # get main categories from the mega category
    main_cat = un_lis.select('div > ul > li')
    for main_cats in main_cat:
        try:
            content = main_cats.contents[1]
        except IndexError:
            content = main_cats.contents[0]
        main_cat_name = content.text.strip()

        try:
            main_cat_uri = content.contents[1].get('href')
        except IndexError:
            main_cat_uri = content.get('href')

        # get sub-categories from main category
        sub_cat = main_cats.select('div > ul > li')
        for sub_cats in sub_cat:
            sub_cat_name = sub_cats.text
            sub_cat_uri = sub_cats.contents[0].get('href')

            data.append({
                'mega_category': mega_cat_name,
                'main_category': main_cat_name,
                'sub_category': sub_cat_name,
                'mega_category_url': mega_cat_uri,
                'main_category_url': main_cat_uri,
                'sub_category_url': sub_cat_uri
            })

# add data into panda dataframe
cat_df = pd.DataFrame(data=data, columns=['mega_category', 'main_category', 'sub_category',
                                          'mega_category_url', 'main_category_url', 'sub_category_url'])


# traverse each sub-category and fetch all the product's price, name, and images
noisy_str = re.compile("[^\d\.]")
product_info = []

for _, sub_cat_urls in cat_df['sub_category_url'].iteritems():
    uri_response = requests.get(url=sub_cat_urls).content
    bs_obj = BeautifulSoup(markup=uri_response, parser='html.parser', features='lxml')

    unordered_product = bs_obj.select('div.product-item')
    for unordered_products in unordered_product:
        if hasattr(unordered_products, 'contents'):
            try:
                product_info.append({
                    'product_name': unordered_products.contents[1].text.strip(),
                    'product_price': float(noisy_str.sub(r'', unordered_products.contents[2].text)),
                    'image_url': unordered_products.contents[0].find('a', href=True).get('href'),
                    'sub_category_url': sub_cat_urls
                })
            except (IndexError, ValueError):
                pass

# add data into panda dataframe
prod_df = pd.DataFrame(data=product_info,
                       columns=['product_name', 'product_price', 'image_url', 'sub_category_url'])
