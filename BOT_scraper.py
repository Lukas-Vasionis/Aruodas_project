import datetime
import pandas as pd
import os
from tqdm import tqdm
from aruodas_lib_2 import scraper_pipeline_utils as sc

def print_all_dfs(obj):
    print(obj.main_data)
    print(obj.crime)
    print(obj.surroundings)

pd.set_option('display.expand_frame_repr', False)

crawl_date_yyyy_mm_dd = datetime.date.today().strftime("%Y_%m_%d")
crawl_date_yyyy_mm_dd = '2022_09_15'
tipas = 'butai'

'''
CREATING URL LIST FOR CRAPING:
a) scrape all URLs in list of crawled URLs
b) scrape only those URLs that were not scraped from list
    b is only for those cases when previous run was terminated in a middle
'''

url_list, all_scr_data = sc.continue_previous_url_list(crawl_date_yyyy_mm_dd, tipas)

driver = sc.get_driver()


for url in tqdm(url_list[0:2]):

    try:
        sc.enter_url(url, driver)
        url_page_data = sc.scraped_data(main_data=None,
                                        crime=None,
                                        surroundings=None)

        url_page_data.scrape_data(driver)
        all_scr_data.update_with_scraped_data(url_page_data, url)

    except Exception as error:
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




