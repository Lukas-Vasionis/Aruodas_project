import datetime
import pandas as pd
from aruodas_lib_2 import utils_crawler as crl
from aruodas_lib_2 import utils_pipeline as sc

pd.set_option('display.expand_frame_repr', True)

tipas = 'butu-nuoma'
miestas = 'vilniuje'
price_min : int = 300
price_max : int = 1000


'''
From the given filter a START_URL is constructed. From here, we start the crawling process.
In the contents START_URL we look for the number of the last page in the page ruler at the buttom of the page.
The page number will be later stored into last_pg_no variable and used for "for" loop.
Before the loop, an empty df is created for storing the urls of ads and additional data.
Inside the loop:

    * Since the START_URL is the same as the 1st page in the page ruler, we go straight to the scraping part
    
    * The rest of the pages are constructed, accessed and then scraped.
    
    * The scraped data is placed into df_url_links
    
The final df gets deduplication and is saved into csv
    
'''

driver = sc.get_driver()

START_URL = crl.set_START_URL(tipas, miestas, price_min, price_max)
sc.enter_url(START_URL, driver)

df_url_links = pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])

last_pg_no = crl.get_last_pg_no(driver)
for pg_no in range(1, last_pg_no + 1):

    if pg_no != 1:
        pg_url=crl.construct_pg_url(START_URL, pg_no)
        crl.go_to_pg_url(pg_url, driver)

    print(f'Crawling over page {pg_no}')
    df_url_links = crl.get_pg_url_links(df_url_links, START_URL, driver)

driver.quit()
df_url_links = df_url_links.drop_duplicates(subset='url')
df_url_links.to_csv(f'data/crawler/{tipas}/{datetime.date.today().strftime("%Y_%m_%d")}_date_crawled.csv', index=False)
print(df_url_links.head())
