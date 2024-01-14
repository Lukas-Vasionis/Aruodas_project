import argparse
import datetime
import pandas as pd
import os
from tqdm import tqdm
from aruodas_lib_2 import utils_pipeline as sc
import argparse

pd.set_option('display.expand_frame_repr', False)
parser = argparse.ArgumentParser()

# User input

# -db DATABASE -u USERNAME -p PASSWORD -size 20
parser.add_argument("-t", "--tipas", help="Type - rent ('butu-nuoma')/sale('butai')")
parser.add_argument("-co", "--c_old_list",
                    help="Continue from last link in previous list that was executed and later terminated for some reason. "
                         "'Y' - will continue frow the last session of crawling date. "
                         "'n' - will itterate all over again"
                         "None - will ask you to enter 'Y' or 'n'")
parser.add_argument("-d", "--crawling_date", help="Set crawling data (yyyy_mm_dd). "
                                                  "If None - value is set as today's date. "
                                                  "This date refers to that crawling file that is named after date of crawling")
args = parser.parse_args()

# tipas = args.tipas
# continue_old_list = args.c_old_list
# crawl_date_as_yyyy_mm_dd = args.crawling_date

tipas = args.tipas
continue_old_list = args.c_old_list
crawl_date_as_yyyy_mm_dd = args.crawling_date

# If none, takes todays date, else: give str in format yyyy_mm_dd
crawl_date_yyyy_mm_dd = sc.get_crawl_date(crawl_date_as_yyyy_mm_dd=crawl_date_as_yyyy_mm_dd)

'''
CREATING URL LIST FOR SCRAPING:
* scrape all URLs in list of crawled URLs
* If the connection is terminated, the scrapped data is stored
    * This script allows you to start from were the scraping process was terminated
'''

# Preparing the data for terminated session. Follow the terminal.

url_list, all_scr_data = sc.continue_previous_url_list(crawl_date_yyyy_mm_dd, tipas,
                                                       continue_old_list=continue_old_list)

driver = sc.get_driver(
    geckodriver_url="https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-win32.zip",
    geckodriver_folder="./other",
    firefox_path='C:/Program Files/Mozilla Firefox/firefox.exe')

for url in tqdm(url_list):
    try:
        sc.enter_url(url, driver)
        # Creating Obj to store data
        page_data = sc.Ad(main_data=None,
                          crime=None,
                          surroundings=None)
        # Scrape data
        page_data.scrape_data(driver)
        # Update previously gathered data
        all_scr_data.update_with_scraped_data(page_data, url)

    except Exception as error:
        # If fails - print failure message and store everything into temproal data folder
        print(f'Failed to scrape this URL: {url}')
        print(f'Error: {error}')

        all_scr_data.to_df()
        all_scr_data.save_all_csv('data/scraper/temporal', crawl_date_yyyy_mm_dd)

        driver.quit()
        exit()

driver.quit()
all_scr_data.to_df()
all_scr_data.save_all_csv('data/scraper/temporal', crawl_date_yyyy_mm_dd)

os.makedirs(f"data/scraper/{tipas}/{crawl_date_yyyy_mm_dd}", exist_ok=True)
all_scr_data.save_all_xlsx(tipas, crawl_date_yyyy_mm_dd)
all_scr_data.save_main_csv(tipas, crawl_date_yyyy_mm_dd)
