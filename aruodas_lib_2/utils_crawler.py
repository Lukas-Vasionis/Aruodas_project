import regex as re
import bs4
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import datetime
import pandas as pd
import random

import pickle
import selenium.webdriver


def start_bot(current_url, driver):
    """
    * Enters current_url and clicks the data consent banner
    :param current_url: URL to start with
    :param driver: webdriver object to open url
    :return: None
    """

    driver.get(current_url)

    # Click the data consent banner
    consent_banner = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    consent_banner[0].click()




def set_START_URL(tipas, miestas, price_max, price_min=None):
    """

    :param tipas: Pardavimo tipas - nuoma ('butu-nuoma') ar pardavimas ('butai')
    :param miestas: Buto vietovė - miestas - kilmininko linksniu (pvz 'vilniuje')
    :param price_max: Viršutinis ieškomos kainos limitas
    :param price_min: Apatinis ieškomos kainos limitas
    :return: None
    """

    if price_min is None:
        current_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMax={price_max}'
    elif price_max is None:
        current_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMin={price_min}'
    else:
        current_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMax={price_max}&FPriceMax={price_min}'
    return current_url


def get_last_pg_no(driver):
    last_pg_no = bs4.BeautifulSoup(driver.page_source, 'xml')
    last_pg_no = last_pg_no.find_all(class_="pagination")[0].find_all("a")
    last_pg_no = [x for x in last_pg_no if x.string != '»'][-1]
    last_pg_no = re.sub(r"[\n\t\s]*", "", last_pg_no.string)
    last_pg_no = int(last_pg_no)

    return last_pg_no

def construct_pg_url(current_url, current_pg_no):
    div_url = current_url.rsplit('/', 1)

    url_root = div_url[0]
    url_end = div_url[1]

    next_url = f'{url_root}/puslapis/{str(current_pg_no)}/{url_end}'
    return next_url

def get_pg_url_links(df_url_ads, current_url, driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find_all(class_="list-search-v2")[0]
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


def go_to_pg_url(pg_url, driver):
    driver.get(pg_url)
    time.sleep(random.uniform(0.5, 1))
