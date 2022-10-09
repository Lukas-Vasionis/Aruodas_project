import time
from bs4 import BeautifulSoup
import os
import regex as re
import pandas as pd
import aruodas_lib_2.get_tbl_library as aruodas

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Initiate the browser
def bot_click():

    options = Options()
    options.headless = False
    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')

    my_url = 'https://www.aruodas.lt/butai/vilniuje/?FPriceMin=100000&FPriceMax=200000'
    driver.get(my_url)
    # time.sleep(2)
    driver.find_element_by_id("onetrust-accept-btn-handler").click()

    def get_list_web(page_source):

        soup = BeautifulSoup(page_source, 'html.parser')
        # print(soup)
        soup = soup.find_all(class_="list-search")[0]
        soup = soup.find_all('a', href=True)
        soup = pd.Series([x['href'] for x in soup])
        soup = soup[~soup.str.contains('luminor|\?FPrice')].unique().tolist()
        list_ulrs = [x for x in soup if x != '#']
        return list_ulrs

    list_urls = get_list_web(driver.page_source)

    for url in list_urls:
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, features="html.parser")
        df_skelbimo_pgr = aruodas.get_tbl_obj_details_v2(soup, 'obj-details')
        print(df_skelbimo_pgr)
        time.sleep(2)

    get_list_web(driver.page_source)

    driver.quit()




bot_click()


def read_html():
    with open('data/compare_source_vs_bs4.html', 'r', encoding='UTF-8') as link:
        link = link.read()

    soup = BeautifulSoup(link, features="html.parser")

    skelbimo_pavadinimas = aruodas.get_skelbimo_pavadinimas(soup)

    df_skelbimo_pgr = aruodas.get_tbl_obj_details_v2(soup, 'obj-details')
    df = skelbimo_datos = aruodas.get_tbl_obj_details_v2(soup, "obj-stats")
    df_artimiausios_istaigos = aruodas.get_df_artimiausios_istaigos(soup)
    df_crime_chart = aruodas.get_crime_chart_data(soup)
    price_eur = aruodas.get_price_eur(soup)
    coordinates = aruodas.get_coordinates(soup)
    skelbimo_perziura = aruodas.get_perziuru_sk(soup)
    skelbimo_tekstas = aruodas.get_skelbimo_tekstas(soup)

    list_my = [skelbimo_pavadinimas, df_skelbimo_pgr, skelbimo_datos, df_artimiausios_istaigos, df_crime_chart,
               price_eur, coordinates, skelbimo_perziura, skelbimo_tekstas]
    for a in list_my:
        print(a)




