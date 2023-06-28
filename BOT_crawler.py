import datetime
import pandas as pd
from aruodas_lib_2 import utils_crawler as crl
from aruodas_lib_2 import utils_pipeline as sc

pd.set_option('display.expand_frame_repr', True)


'''
Crawls over the search result pages that matched the defined filters and stores their URLs into pandas dataframe   
'''
# User input

tipas = 'butai'
miestas = 'vilniuje'
price_min : int = None
price_max : int = None


# The script

driver = sc.get_driver()

# From the given filter a START_URL is constructed. From here, we start the crawling process.
START_URL = crl.set_START_URL(tipas, miestas, price_min, price_max)
sc.enter_url(START_URL, driver)


df_url_links = pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])# Creates an empty pd.Dataframe to store url data
# In the contents START_URL we look for the number of the last page in the page ruler at the buttom of the page.
# This lets to create for loop to itterate over the all search pages.

last_pg_no = crl.get_last_pg_no(driver)

for pg_no in range(1, last_pg_no + 1):

        # Since the START_URL is the same as the 1st page in the search results, we apply url constuction to 2nd and later pages
        if pg_no != 1:
            pg_url=crl.construct_pg_url(START_URL, pg_no) # Constructs the page
            crl.go_to_pg_url(pg_url, driver) # Goes to the page

        print(f'Crawling over search results: page {pg_no}')
        # Scrape search results: URLs of Ads, crawl date, URL of search results
        df_url_links = crl.get_pg_url_links(df_url_links, START_URL, driver)

driver.quit()

# Clean and store collected data
df_url_links = df_url_links.drop_duplicates(subset='url')
df_url_links.to_csv(f'data/crawler/{tipas}/{datetime.date.today().strftime("%Y_%m_%d")}_date_crawled.csv', index=False)
print(df_url_links.head())
