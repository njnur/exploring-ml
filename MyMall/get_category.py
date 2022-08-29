import requests
import psycopg2
import pandas as pd

from bs4 import BeautifulSoup


MYMALL_MEGA_CAT_URI = "https://mymall.se/media/mymall/megamenu/9826648.html"

data = []
uri_response = requests.get(url=MYMALL_MEGA_CAT_URI).content
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
    df = pd.DataFrame(data=data, columns=['mega_category', 'main_category', 'sub_category',
                                          'mega_category_url', 'main_category_url', 'sub_category_url'])
