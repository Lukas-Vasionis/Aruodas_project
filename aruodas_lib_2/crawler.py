import os.path
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import datetime
import pandas as pd
import random

import pickle
import selenium.webdriver





def start_bot(current_url, driver, cookie_path):
    """
    Opens the target url and checks weather the cookies are up-to-date (weather it needs to click the banner of data usage consent):

    * first it checks weather the cookie file exists:

        * if yes, it loads it to the driver

    * Second, it checks weather a cookies are up-to-date by checking if banner pops out

        * If yes - cookies are out-dated: clicks the banned, updates cookies and loads it to the driver

        * If not, it clicks the banner and saves cookies

    :param current_url: URL to start with
    :param cookie_path: cookies
    :param driver: webdriver object to open url
    :return: None
    """

    def update_cookies(action, driver, cookie_path):
        '''

        :param action: Chooaw weather to write or read cookies
        :param driver: webdriver object
        :param cookie_path: path to cookies (to save or to read)
        :return: none
        '''
        if action == 'write':
            pickle.dump(driver.get_cookies(), open(cookie_path, "wb+"))
            print('Writing cookies...')
        elif action == 'read':
            cookies = pickle.load(open(cookie_path, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            print('Loading cookies...')

    driver.get(current_url)

    # If cookies exist - load it
    if os.path.exists(cookie_path):
        driver.get(current_url)
        update_cookies(action='read', driver=driver, cookie_path=cookie_path)
        driver.get(current_url)

    # If banner pops out - click it, update cookies and load them
    consent_banner = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
    if consent_banner:
        consent_banner[0].click()
        time.sleep(1)
        update_cookies(action='write', driver=driver, cookie_path=cookie_path)
        update_cookies(action='read', driver=driver, cookie_path=cookie_path)
        driver.get(current_url)
        input("i?")
    driver.get(current_url)

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
