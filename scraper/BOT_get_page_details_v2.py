import datetime

from bs4 import BeautifulSoup
from collections import Counter
import pandas as pd
import aruodas_lib_2.get_tbl_library as aruodas
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from tqdm import tqdm

pd.set_option('display.expand_frame_repr', False)

crawl_date_yyyy_mm_dd = datetime.date.today().strftime("%Y_%m_%d")
# crawl_date_yyyy_mm_dd = '2022_10_08'


def get_raw_urls():
    par_dir = os.path.dirname(os.getcwd())
    name_df = f'date_crawled_{crawl_date_yyyy_mm_dd}.csv'
    df_crawled = pd.read_csv(f'{par_dir}/crawler/data/{name_df}')
    url_list = df_crawled['url'].to_list()
    return url_list


def get_scraped_ulrs():
    temp_data = [x for x in os.listdir('data/temporal/') if crawl_date_yyyy_mm_dd in x]
    scraped_urls = []

    for df in temp_data:
        df = pd.read_csv(f'data/temporal/{df}')
        list_url = df['url_crawl'].tolist()
        list_url = list(set(list_url))
        scraped_urls = scraped_urls + list_url

    counts = Counter(scraped_urls)
    scraped_urls = [value for value, count in counts.items() if count == 3]
    return scraped_urls


def enter_url(url):
    # url = 'https://www.aruodas.lt/butai/vilniuje/?FPriceMin=100000&FPriceMax=200000'
    driver.get(url)
    time.sleep(0.5)
    try:
        driver.find_element_by_id("onetrust-accept-btn-handler").click()
    except:
        pass


def scrape_data():
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    skelbimo_pavadinimas = aruodas.get_skelbimo_pavadinimas(soup)
    df_skelbimo_santrauka = aruodas.get_tbl_obj_details_v2(soup, 'obj-details')
    df_skelbimo_datos = aruodas.get_tbl_obj_details_v2(soup, "obj-stats")
    price_eur = aruodas.get_price_eur(soup)
    coordinates = aruodas.get_coordinates(soup)
    skelbimo_perziura = aruodas.get_perziuru_sk(soup)
    skelbimo_tekstas = aruodas.get_skelbimo_tekstas(soup)
    e_klase = aruodas.get_energy_consumption_class(soup)
    oro_tarsa = aruodas.get_air_polution_data(soup)
    df_main_data = pd.concat([skelbimo_pavadinimas, price_eur, df_skelbimo_santrauka, df_skelbimo_datos, coordinates,
                              skelbimo_perziura, e_klase, oro_tarsa,
                              skelbimo_tekstas
                              ], axis=1)
    df_main_data.loc[:, 'url_crawl'] = driver.current_url

    df_crime = aruodas.get_crime_chart_data(soup)
    df_crime.loc[:, 'url_crawl'] = driver.current_url

    df_surroundings = aruodas.get_df_artimiausios_istaigos(soup)
    df_surroundings.loc[:, 'url_crawl'] = driver.current_url

    return {'df_main_data': df_main_data,
            'df_crime': df_crime,
            'df_surroundings': df_surroundings}


def save_all_csv(file_path):
    df_all_scraped_main.to_csv(f'{file_path}/scraped_main_{crawl_date_yyyy_mm_dd}.csv', index=False)
    df_all_scraped_crime.to_csv(f'{file_path}/scraped_crime_{crawl_date_yyyy_mm_dd}.csv', index=False)
    df_all_scraped_surroundings.to_csv(f'{file_path}/scraped_surroundings_{crawl_date_yyyy_mm_dd}.csv', index=False)


def save_all_xlsx(file_name):
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df_all_scraped_main.to_excel(writer, sheet_name='scraped_main_data', index=False)
    df_all_scraped_crime.to_excel(writer, sheet_name='scraped_crime_data', index=False)
    df_all_scraped_surroundings.to_excel(writer, sheet_name='scraped_surroundings_data', index=False)
    writer.save()


def save_main_csv(file_name):
    df_all_scraped_main.to_csv(file_name, index=False, sep=';')

'''
CREATING URL LIST FOR CRAPING:
a) scrape all URLs in list of crawled URLs
b) scrape only those URLs that were not scraped from list
    b is only for those cases when previous run was terminated in a middle
'''

continue_old_list = input("Continue previously failed session? "
                          "\n(Useful if previous execution was interrupted)"
                          "\nType Y/n:")
if continue_old_list == 'Y':
    raw_url_list = get_raw_urls()
    scarped_urls = set(get_scraped_ulrs())

    urls_not_scraped = [x for x in raw_url_list if x not in scarped_urls]
    url_list = urls_not_scraped

    df_all_scraped_main = pd.read_csv(f'data/temporal/scraped_main_{crawl_date_yyyy_mm_dd}.csv')
    df_all_scraped_crime = pd.read_csv(f'data/temporal/scraped_crime_{crawl_date_yyyy_mm_dd}.csv')
    df_all_scraped_surroundings = pd.read_csv(f'data/temporal/scraped_surroundings_{crawl_date_yyyy_mm_dd}.csv')

elif continue_old_list == 'n':
    print('Parsing thorugh all URLs again')
    url_list = get_raw_urls()
    df_all_scraped_main = pd.DataFrame(columns=['url_crawl'])
    df_all_scraped_crime = pd.DataFrame(columns=['url_crawl'])
    df_all_scraped_surroundings = pd.DataFrame(columns=['url_crawl'])
else:
    print("Invalid input")
    exit()

'''
SCRAPING
'''
options = Options()
options.headless = False
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

for url in tqdm(url_list[0:5]):
    enter_url(url)
    df_url_scraped = scrape_data()

    df_all_scraped_main = pd.concat([df_all_scraped_main, df_url_scraped['df_main_data']], axis=0).reset_index(
        drop=True)
    df_all_scraped_crime = pd.concat([df_all_scraped_crime, df_url_scraped['df_crime']], axis=0).reset_index(drop=True)
    df_all_scraped_surroundings = pd.concat([df_all_scraped_surroundings, df_url_scraped['df_surroundings']],
                                            axis=0).reset_index(drop=True)
    save_all_csv(f'data/temporal')
driver.quit()
df_all_scraped_main.loc[:, 'scrape_date'] = datetime.date.today().strftime("%Y_%m_%d")
df_all_scraped_crime.loc[:, 'scrape_date'] = datetime.date.today().strftime("%Y_%m_%d")
df_all_scraped_surroundings.loc[:, 'scrape_date'] = datetime.date.today().strftime("%Y_%m_%d")

'''
SAVING
'''
if os.path.exists(f"data/{crawl_date_yyyy_mm_dd}")==False:
    os.mkdir(f"data/{crawl_date_yyyy_mm_dd}")

save_all_xlsx(f'data/{crawl_date_yyyy_mm_dd}/scraped_all_{crawl_date_yyyy_mm_dd}.xlsx')
save_main_csv(f'data/{crawl_date_yyyy_mm_dd}/scraped_main_{crawl_date_yyyy_mm_dd}.csv')
# print(df_all_scraped.to_markdown())
#
