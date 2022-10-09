import datetime
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random

from webdriver_manager.chrome import ChromeDriverManager

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_colwidth', 1000)

def start_bot(curr_url):
    driver.get(curr_url)
    time.sleep(1)
    driver.find_element(By.ID,"onetrust-accept-btn-handler").click()
    time.sleep(1)


def get_curr_url_links(df_url_ads,curr_url):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    soup = soup.find_all(class_="list-search")[0]
    soup = soup.find_all('a', href=True)
    soup = pd.Series([x['href'] for x in soup])
    soup = soup[~soup.str.contains('luminor|\?FPrice|^/')].unique().tolist()
    list_ulrs = [x for x in soup if x != '#']

    df_new_url=pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])

    df_new_url.loc[:,'url']=list_ulrs
    df_new_url.loc[:,'date_crawled']=datetime.date.today().strftime("%Y-%m-%d")
    df_new_url.loc[:, 'first_search_url']=curr_url
    df_url_ads=pd.concat([df_url_ads, df_new_url])
    return df_url_ads


def get_next_page_url(curr_url):
    # curr_url = driver.current_url
    if 'puslapis' not in curr_url:
        curr_url = curr_url.rsplit('/', 1)
        next_url = curr_url[0] + f'/puslapis/2/' + curr_url[1]
    else:
        div_url = curr_url.rsplit('/', 1)
        url_root = div_url[0].rsplit('/', 1)[0]
        num = div_url[0].rsplit('/', 1)[1].strip()
        print(f'Page {num}')
        url_end = div_url[1]
        next_url = f'{url_root}/{int(num) + 1}/{url_end}'
    return next_url


def go_to_next_page_url(next_url):
    driver.get(next_url)


def get_curr_page_url():
    curr_url = driver.current_url
    return(curr_url)


tipas='butu-nuoma'
miestas='vilniuje'
price_max='1000'
price_min='300'

curr_url = f'https://www.aruodas.lt/{tipas}/{miestas}/?FPriceMax={price_max}&FPriceMax={price_min}'
print(curr_url)
# curr_url = 'https://www.aruodas.lt/butai/vilniuje/puslapis/76/?FPriceMin=100000'
# curr_url = 'https://www.aruodas.lt/butai/vilniuje/'
next_url_generated = get_next_page_url(curr_url)

next_url_resulted = next_url_generated
df_url_ads=pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])

options = Options()
options.headless = False

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
start_bot(curr_url)

while next_url_resulted == next_url_generated:
    curr_url = get_curr_page_url()

    df_url_ads = get_curr_url_links(df_url_ads, curr_url)

    next_url_generated = get_next_page_url(curr_url)
    go_to_next_page_url(next_url_generated)
    time.sleep(random.uniform(3, 4))
    next_url_resulted = get_curr_page_url()
    # time.sleep(5)

driver.quit()
df_url_ads = df_url_ads.drop_duplicates(subset='url')
df_url_ads.to_csv(f'data/{tipas}/date_crawled_{datetime.date.today().strftime("%Y_%m_%d")}.csv', index=False)
print(df_url_ads.to_markdown())
