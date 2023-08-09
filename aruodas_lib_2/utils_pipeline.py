from . import utils_page_scraper as pg_scraper
import os
import time
import lxml
import datetime
import pandas as pd
from collections import ChainMap, Counter
from pandas import read_csv, DataFrame, concat, ExcelWriter
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# scraped_data
class Ad:
    def __init__(self, main_data, crime, surroundings):
        """
        :param main_data: data about apartments location, description etc.
        :param crime: crime statistics in the area
        :param surroundings: statistics about kindergardens, shops, bus stops etc. arround the appartment
        """

        self.main_data = main_data
        self.crime = crime
        self.surroundings = surroundings

    def make_from_temp_folder(self, crawl_date_yyyy_mm_dd):
        """
        This functions reads the data from previously terminated session that is saved into data/scraper/temporal.
        :param crawl_date_yyyy_mm_dd: date of the terminated session
        :return: self
        """
        self.main_data = read_csv(f'data/scraper/temporal/{crawl_date_yyyy_mm_dd}_scraped_main.csv')
        self.crime = read_csv(f'data/scraper/temporal/{crawl_date_yyyy_mm_dd}_scraped_crime.csv')
        self.surroundings = read_csv(f'data/scraper/temporal/{crawl_date_yyyy_mm_dd}_scraped_surroundings.csv')

        self.main_data = self.main_data.to_dict('records')

        self.crime = self.crime.values.tolist()
        self.surroundings = self.surroundings.values.tolist()
        return self


    def scrape_data(self, driver):
        '''
        Scrapes the data using funcs from scraper_page_scraper and concat it into 3 datasets of class Ad

        :param driver: webdriver object
        :return: self with scraped data of the page that the webdriver object is on.
        '''
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # First we create the separate objects with info about Ad. Every variable is a dict
        skelbimo_pavadinimas = pg_scraper.get_skelbimo_pavadinimas(soup)
        skelbimo_santrauka = pg_scraper.get_tbl_obj_details_v2(soup, 'obj-details')
        skelbimo_statistika = pg_scraper.get_tbl_obj_details_v2(soup, "obj-stats") 
        price_eur = pg_scraper.get_price_eur(soup)
        coordinates = pg_scraper.get_coordinates(soup)
        skelbimo_perziura = pg_scraper.get_perziuru_sk(soup)
        skelbimo_tekstas = pg_scraper.get_skelbimo_tekstas(soup)
        e_klase = pg_scraper.get_energy_consumption_class(soup) # Energy class
        oro_tarsa = pg_scraper.get_air_polution_data(soup)
        url_crawl = driver.current_url # Url with which one enters the page

        # Later, these objects are joined together into three datasets: main_data, crime, surroundings
        self.main_data = skelbimo_pavadinimas | skelbimo_santrauka | skelbimo_statistika | price_eur | coordinates | \
                         skelbimo_perziura | skelbimo_tekstas | e_klase | oro_tarsa | {'url_crawl': url_crawl}

        self.crime = pg_scraper.get_crime_chart_data(soup)
        self.crime = [[url_crawl] + row for row in self.crime]

        self.surroundings = pg_scraper.get_df_artimiausios_istaigos(soup)
        self.surroundings = [[url_crawl] + row for row in self.surroundings]
        return self

    def update_with_scraped_data(self, scraped_data_upd, url):

        if 'error_get_skelbimo_pavadinimas' in scraped_data_upd.main_data:
            print(f'Failed to scrape this URL: {url}')
            pass
        else:
            self.main_data = self.main_data + [scraped_data_upd.main_data]
            self.crime = self.crime + scraped_data_upd.crime
            self.surroundings = self.surroundings + scraped_data_upd.surroundings
            return self

    def clean_df(self):
        self.surroundings.loc[:, 'istaigos_tipas'] = self.surroundings['istaigos_tipas'].str.replace('\s{2,}', ' ',
                                                                                                     regex=True)

        return self

    def add_scrape_date(self):
        self.main_data.loc[:, 'scrape_date'] = datetime.date.today().strftime("%Y_%m_%d")
        self.crime.loc[:, 'scrape_date'] = datetime.date.today().strftime("%Y_%m_%d")
        self.surroundings.loc[:, 'scrape_date'] = datetime.date.today().strftime("%Y_%m_%d")
        return self

    def to_df(self):

        self.main_data = pd.DataFrame(self.main_data)
        self.crime = pd.DataFrame(self.crime, columns=['url_crawl','Mėn.','Nusikaltimai 500 m spinduliu','periodas', 'error', "scrape_date"])
        self.surroundings = pd.DataFrame(self.surroundings, columns=['url_crawl','atstumas_km','istaiga','istaigos_tipas',"scrape_date"])
        self.clean_df()
        self.add_scrape_date()
        return self

    def save_all_csv(self, file_path, crawl_date_yyyy_mm_dd):
        self.main_data.to_csv(f'{file_path}/{crawl_date_yyyy_mm_dd}_scraped_main.csv', index=False)
        self.crime.to_csv(f'{file_path}/{crawl_date_yyyy_mm_dd}_scraped_crime.csv', index=False)
        self.surroundings.to_csv(f'{file_path}/{crawl_date_yyyy_mm_dd}_scraped_surroundings.csv', index=False)
        return self

    def save_all_xlsx(self, tipas, crawl_date_yyyy_mm_dd):
        file_name = f'data/scraper/{tipas}/{crawl_date_yyyy_mm_dd}/{crawl_date_yyyy_mm_dd}_scraped_all.xlsx'
        writer = ExcelWriter(file_name, engine='xlsxwriter',
                        engine_kwargs = {'options': {'strings_to_urls': False}})
        self.main_data.to_excel(writer, sheet_name='scraped_main_data', index=False)
        self.crime.to_excel(writer, sheet_name='scraped_crime_data', index=False)
        self.surroundings.to_excel(writer, sheet_name='scraped_surroundings_data', index=False)
        writer.close()
        return self

    def save_main_csv(self, tipas, crawl_date_yyyy_mm_dd):
        file_name = f'data/scraper/{tipas}/{crawl_date_yyyy_mm_dd}/{crawl_date_yyyy_mm_dd}_scraped_main.csv'
        self.main_data.to_csv(file_name, index=False, sep=';')
        return self



def get_crawl_date(crawl_date_as_yyyy_mm_dd=None):
    if crawl_date_as_yyyy_mm_dd is None:
        crawl_date_as_yyyy_mm_dd = datetime.date.today().strftime("%Y_%m_%d")
    else:
        crawl_date_as_yyyy_mm_dd = crawl_date_as_yyyy_mm_dd

    return crawl_date_as_yyyy_mm_dd


def continue_previous_url_list(crawl_date_yyyy_mm_dd, tipas, continue_old_list=None):
    '''
    Lets you choose to continue scraping urls from previously terminated session
    '''

    def get_raw_urls():
        name_df = f'{crawl_date_yyyy_mm_dd}_date_crawled.csv'
        df_crawled = read_csv(f'data/crawler/{tipas}/{name_df}')
        url_list = df_crawled['url'].to_list()
        return url_list

    def get_scraped_ulrs():
        def get_list_urls(df_name):
            df = read_csv(f'./data/scraper/temporal/{df_name}')
            list_url = df['url_crawl'].tolist()
            list_url = list(set(list_url))
            return list_url

        print(os.getcwd())
        names_of_files = [x for x in os.listdir('./data/scraper/temporal') if crawl_date_yyyy_mm_dd in x]
        scraped_urls = [get_list_urls(x) for x in names_of_files]
        scraped_urls = [j for i in scraped_urls for j in i]

        counts = Counter(scraped_urls)
        scraped_urls = [value for value, count in counts.items() if count == 3]
        return scraped_urls

    if continue_old_list is None:
        continue_old_list = input("Continue previously failed session? "
                                  "\n(Useful if previous execution was interrupted)"
                                  "\nType Y/n:")

    raw_url_list = get_raw_urls()

    if continue_old_list == 'Y':

        scarped_urls = set(get_scraped_ulrs())
        urls_not_scraped = [x for x in raw_url_list if x not in scarped_urls]

        url_list = urls_not_scraped
        scr_data = Ad(main_data=[], crime=[], surroundings=[])
        scr_data.make_from_temp_folder(crawl_date_yyyy_mm_dd)

    elif continue_old_list == 'n':
        print('Parsing through all URLs again')

        url_list = raw_url_list
        scr_data = Ad(main_data=[], crime=[], surroundings=[])
    else:
        print("Invalid input")
        exit()
    return url_list, scr_data

from selenium.webdriver.firefox.options import Options as FirefoxOptions


def get_driver():
    options = FirefoxOptions()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    return driver


def enter_url(url, driver):
    driver.get(url)
    try:
        consent_banner = driver.find_elements(By.ID, "onetrust-accept-btn-handler")
        consent_banner[0].click()
    except:
        pass

def get_html(url_index, url, driver):
    driver.get(url)
    try:
        time.sleep(0.3)
        driver.find_element('id', "onetrust-accept-btn-handler").click()
    except:
        pass
    source = driver.page_source
    with open(f"other/html/{url_index}_page_source", "w", encoding='utf-8') as fileToWrite:
        fileToWrite.write(source)
    print("wrote")