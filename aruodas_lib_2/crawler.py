import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import datetime
import pandas as pd
import random


def start_bot(current_url, driver):
    driver.get(current_url)
    time.sleep(1)
    driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    time.sleep(1)


def set_current_url(tipas, miestas, price_max, price_min=None):
    if price_min == None:
        current_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMax={price_max}'
    elif price_max == None:
        current_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMin={price_min}'
    else:
        current_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMax={price_max}&FPriceMax={price_min}'
    return current_url


def get_current_url_links(df_url_ads, current_url, driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find_all(class_="list-search")[0]
    soup = soup.find_all('a', href=True)
    soup = pd.Series([x['href'] for x in soup])
    soup = soup[~soup.str.contains('luminor|\?FPrice|^/')].unique().tolist()
    list_ulrs = [x for x in soup if x != '#']

    df_new_url = pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])

    df_new_url.loc[:, 'url'] = list_ulrs
    df_new_url.loc[:, 'date_crawled'] = datetime.date.today().strftime("%Y-%m-%d")
    df_new_url.loc[:, 'first_search_url'] = current_url
    df_url_ads = pd.concat([df_url_ads, df_new_url])
    return df_url_ads


def get_next_page_url(current_url):
    if 'puslapis' not in current_url:
        current_url = current_url.rsplit('/', 1)
        next_url = current_url[0] + f'/puslapis/2/' + current_url[1]
    else:
        div_url = current_url.rsplit('/', 1)
        url_root = div_url[0].rsplit('/', 1)[0]
        num = div_url[0].rsplit('/', 1)[1].strip()
        print(f'Page {num}')
        url_end = div_url[1]
        next_url = f'{url_root}/{int(num) + 1}/{url_end}'
    return next_url


def go_to_next_page_url(next_url, driver):
    driver.get(next_url)
    time.sleep(random.uniform(3, 4))


def get_current_page_url(driver):
    current_url = driver.current_url
    return (current_url)
