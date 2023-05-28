import datetime
import pandas as pd
from aruodas_lib_2 import crawler as crl
from aruodas_lib_2 import scraper_pipeline_utils as sc

pd.set_option('display.expand_frame_repr', True)

tipas = 'butu-nuoma'
miestas = 'vilniuje'
price_max = 1000
price_min = 300

current_url = crl.set_current_url(tipas, miestas, price_min, price_max)
# current_url='https://www.aruodas.lt/butu-nuoma/vilniuje/puslapis/63/?FPriceMax=300&FPriceMax=1000'

driver = sc.get_driver()
crl.start_bot(current_url, driver, cookie_path="./cookies/cookies.pkl")
input('c?')
'''
Crawling through the pages has the following logic:
The crawler parses through the pages by clicking page element in the ruller at the bottom of the current page.
When the last page is clicked (let say pg 13), the next page will lead you back the 13.
Therfore, we check     
'''
# next_url_generated = crl.get_next_page_url(current_url)
# next_url_resulted = next_url_generated
next_url_generated = None
next_url_resulted = None


df_url_links = pd.DataFrame(columns=['url', 'date_crawled', 'first_search_url'])

while next_url_resulted == next_url_generated:
    current_url = crl.get_current_page_url(driver)

    df_url_links = crl.get_current_url_links(df_url_links, current_url, driver)

    next_url_generated = crl.get_next_page_url(current_url)
    crl.go_to_next_page_url(next_url_generated, driver)
    next_url_resulted = crl.get_current_page_url(driver)

driver.quit()
df_url_links = df_url_links.drop_duplicates(subset='url')
df_url_links.to_csv(f'data/crawler/{tipas}/{datetime.date.today().strftime("%Y_%m_%d")}_date_crawled.csv', index=False)
print(df_url_links.head())
