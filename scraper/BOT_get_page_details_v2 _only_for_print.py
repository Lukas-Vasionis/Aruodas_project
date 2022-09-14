import datetime

from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import aruodas_lib_2.get_tbl_library as aruodas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

pd.set_option('display.expand_frame_repr', False)

crawl_date_dd_mm_yyyy = '13_09_2022'


def access_url_df(crawl_date_dd_mm_yyyy):
    par_dir = os.path.dirname(os.getcwd())
    name_df = f'date_crawled_{crawl_date_dd_mm_yyyy}.csv'
    df_crawled = pd.read_csv(f'{par_dir}/crawler/data/{name_df}')
    return df_crawled


def enter_url(url):
    # url = 'https://www.aruodas.lt/butai/vilniuje/?FPriceMin=100000&FPriceMax=200000'
    driver.get(url)
    time.sleep(1)
    try:
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
    except:
        pass
    time.sleep(1)


def scrape_data():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(aruodas.get_df_artimiausios_istaigos(soup))
    print(aruodas.get_crime_chart_data(soup))
    # skelbimo_pavadinimas = aruodas.get_skelbimo_pavadinimas(soup)
    # df_skelbimo_santrauka = aruodas.get_tbl_obj_details_v2(soup, 'obj-details')
    # df_skelbimo_datos = aruodas.get_tbl_obj_details_v2(soup, "obj-stats")
    # price_eur = aruodas.get_price_eur(soup)
    # coordinates = aruodas.get_coordinates(soup)
    # skelbimo_perziura = aruodas.get_perziuru_sk(soup)
    # skelbimo_tekstas = aruodas.get_skelbimo_tekstas(soup)
    # e_klase = aruodas.get_energy_consumption_class(soup)
    # oro_tarsa = aruodas.get_air_polution_data(soup)
    # df_scraped = pd.concat([skelbimo_pavadinimas, price_eur, df_skelbimo_santrauka, df_skelbimo_datos, coordinates,
    #                         skelbimo_perziura, e_klase, oro_tarsa,
    #                         skelbimo_tekstas
    #                         ], axis=1)
    # df_scraped.loc[:, 'url_crawl'] = driver.current_url
    # return df_scraped

options = Options()
options.headless = False
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

list_crawled_url = access_url_df('13_09_2022')['url'].to_list()
# list_crawled_url = list_crawled_url[0:2]

df_all_scraped = pd.DataFrame(columns=['url_crawl'])

for url in list_crawled_url[0:1]:
    enter_url(url)
    df_url_scraped = scrape_data()
    df_all_scraped = pd.concat([df_all_scraped, df_url_scraped], axis=0).reset_index(drop=True)

driver.quit()
# df_all_scraped.loc[:, 'scrape_date'] = datetime.date.today().strftime("%d_%m_%Y")
# df_all_scraped.to_csv(f'data/scraped_date_crawled_{crawl_date_dd_mm_yyyy}.csv', index=False, sep=';')
# print(df_all_scraped.to_markdown())