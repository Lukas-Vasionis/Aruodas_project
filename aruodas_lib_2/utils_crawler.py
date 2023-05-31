import time
import pandas as pd
import regex as re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import datetime
import random

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
    Sukonstruoja pirminį url padal suvestus filtrus

    :param tipas: Pardavimo tipas - rent ('butu-nuoma') ar pardavimas ('butai')
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
    """
    Pradiniame puslapyje suranda puslapių sąrašą (angliškai vadinu page ruller) ir paima jo paskutinį narį. Taip sužinom apie puslapių skaičių

    :param driver:
    :return:
    """
    last_pg_no = BeautifulSoup(driver.page_source, 'xml')
    last_pg_no = last_pg_no.find_all(class_="pagination")[0].find_all("a")
    last_pg_no = [x for x in last_pg_no if x.string != '»'][-1]
    last_pg_no = re.sub(r"[\n\t\s]*", "", last_pg_no.string)
    last_pg_no = int(last_pg_no)

    return last_pg_no


def construct_pg_url(current_url, current_pg_no):
    """
    Iš puslapio URL ir puslapio numerio sukuria einamojo puslapio url

    :param current_url: webdriver objekte užkrauto puslapio URL
    :param current_pg_no: puslapio (tą kurį reikia užkrauti) numeris
    :return next_url: puslapio, kurį reikia užkrauti, URL
    """
    div_url = current_url.rsplit('/', 1)

    url_root = div_url[0]
    url_end = div_url[1]

    next_url = f'{url_root}/puslapis/{str(current_pg_no)}/{url_end}'
    return next_url

def go_to_pg_url(next_url, driver):
    """
    Goes to url that was constructed inside construct_pg_url()

    :param next_url: The url that was constructed inside construct_pg_url()
    :param driver: webdriver opj
    :return: None
    """
    driver.get(next_url)
    time.sleep(random.uniform(0.5, 1))

def get_pg_url_links(df_url_ads, current_url, driver):
    """
    Stores Ad URLs that were found in the current_url

    :param df_url_ads: Pandas dataframe to store crawler scrapped data
    :param current_url: URL of the page, from which Ad links are taken
    :param driver: Webdriver obj
    :return: pd.Dataframe with replenished data
    """

    soup = BeautifulSoup(driver.page_source, 'html.parser') # Gets the page source
    soup = soup.find_all(class_="list-search-v2")[0] # Subsets the object with Ads

    # Extracts the links
    soup = soup.find_all('a', href=True)
    soup = pd.Series([x['href'] for x in soup])

    # Discards the rubbish
    soup = soup[~soup.str.contains('luminor|\?FPrice|^/')].unique().tolist()
    list_ulrs = [x for x in soup if x != '#']

    # Creates new df and stores the links data
    df_new_url = pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])

    df_new_url.loc[:, 'url'] = list_ulrs    #Stores the links to Ads
    df_new_url.loc[:, 'date_crawled'] = datetime.date.today().strftime("%Y-%m-%d")  # Marks the crawling date
    df_new_url.loc[:, 'first_search_url'] = current_url # Marks the url of page where the add is found

    # Adds new data to the previously collected data
    df_url_ads = pd.concat([df_url_ads, df_new_url])
    return df_url_ads


