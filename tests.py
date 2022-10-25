import os

import pandas as pd
from pandas.errors import InvalidIndexError

# options = Options()
# options.headless = False
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
pd.set_option('display.expand_frame_repr', False)
from scraper.aruodas_lib_2 import scraper as sc

url_0 = 'https://www.aruodas.lt/butu-nuoma-vilniuje-antakalnyje-stepono-kairio-g-500-eur-su-komunaliniais-nuomojamas-kambarys-4-1184780/'
url_1 = 'https://www.aruodas.lt/butu-nuoma-vilniuje-seskineje-musninku-g-nuomojamas-jaukus-ir-tvarkingas-po-remonto-1-4-1187106/'
url_2 = 'https://www.aruodas.lt/butu-nuoma-vilniuje-senamiestyje-dominikonu-g-kompaktiskas-prestizinis-dizainerio-kurtas-4-1175193/'


# url = 'view-source:'+url
#
# print(url)
# sc.enter_url(url, driver)
# # soup = BeautifulSoup(driver.page_source, 'html.parser')
# # skelbimo_pavadinimas = aruodas.get_skelbimo_pavadinimas(soup)
# print(BeautifulSoup(driver.page_source, 'html.parser').prettify())
# print(driver.page_source)
# driver.quit()

# dict_0={}
# dict_1={'skelbimo_pavadinimas': 'Kaunas, Freda, T. Ivanausko g., 3 kambarių butas', 'Namo numeris:': '59', 'Plotas:': '81,64 m²', 'Kambarių sk.:': '3', 'Aukštas:': '3', 'Aukštų sk.:': '3', 'Metai:': '2012', 'Pastato tipas:': 'Mūrinis', 'Šildymas:': 'Dujinis', 'Įrengimas:': 'Įrengtas', 'Nuoroda': 'www.aruodas.lt/1-3242301', 'Įdėtas': '2022-10-13', 'Redaguotas': '2022-10-13', 'Įsiminė': ['26'], 'Peržiūrėjo': '626/83 (iš viso/šiandien)', 'kaina_eur': 165000, 'coordinate_x': 54.864901, 'coordinate_y': 23.91818, 'Skelbimą peržiūrėjo (iš viso/šiandien)': ['626/83'], 'Skelbimo tekstas': 'PARDUODAMAS 3-JŲ KAMBARIŲ BUTAS PUIKIOJE VIETOJE FREDOJE!Parduodamas tvarkingas 3-jų kambarių butas Fredoje. Butui priklauso sandėliukas ir parkavimo vieta požeminiame parkinge! Kiemas naujai išklotas trinkelėmis iki pat pagrindinės gatvės, geras privažiavimas, rami vieta. Butas yra šiltas ir šviesus, nedideli šildymo mokesčiai žiemą. Aukšte yra tik vienas butas, visoje laiptinėje tik trys butai!\n-----------------------------\nPRIVALUMAI:\n- Šildomos grindys;\n- Nerasoja langai prie radiatorių, nes po plytelėmis šildomos grindys;\n- Spintoje po plytelėmis šildomos grindys;\n- Vidaus sienos - mūrinės;\n- Dujinis katilas yra ne momentinis, o su 50L talpa, tad visuomet yra paruoštas karštas vanduo;\n- Kieme iki pat asfaltuotos gatvės bus išklotos trinkelės (jau sumokėti pinigai);\n- Namo pirmininkas, kuris rūpinasi visais iškilusiais klausimais;\n- Butui priklauso sandėliukas;\n- Butui priklauso parkavimo vieta požeminiame parkinge;\n- Nedideli šildymo mokesčiai;\n- Tik vienas butas aukšte;\n- Aukštos lubos;\n- Butas nereikalauja jokių papildomų investicijų;\n- Rami vieta;\n- Išvystyti dviračių takai, kuriais galite pasiekti centrą ir visus kitus mikrorajonus dviračiu;\n- Oro tarša: labai žema (šalt. www.kurgyvenu.lt)\n-----------------------------\nBENDRA INFORMACIJA:\n- Statybos metai: 2012\n- Kambarių sk.: 3\n- Aukštas: 3/3\n- Plotas: 81.64 m²\n- Šildymas: dujinis\n-----------------------------\nATSTUMAI:\n~3.84 km. Atstumas iki centro\n~2.75 km. Kauno Autobusų stotis\n~2.46 km. Kauno keleivinė geležinkelio stotis\n-----------------------------\n• Jeigu norite sužinoti daugiau informacijos ar sutarti laiką apžiūrai, susisiekime Jums patogiu metu!\n• Galiu padėti gauti finansavimą šiam būstui įsigyti!\n• Esant poreikiui galiu parduoti ir Jūsų turtą!', 'error_get_energy_consumption_class': "'NoneType' object has no attribute 'text'", 'Azoto dioksidas (NO2)': '10.3 µg/m3', 'Kietosios dalelės (KD10)': '30.2 µg/m3', 'url_crawl': 'https://www.aruodas.lt/butai-kaune-fredoje-t-ivanausko-g-parduodamas-3-ju-kambariu-butas-puikioje-1-3242301/'}
# dict_2={ 'Plotas:': '81,64 m²', 'Kambarių sk.:': '3', 'Aukštas:': '3', 'Aukštų sk.:': '3', 'Metai:': '2012', 'Pastato tipas:': 'Mūrinis', 'Šildymas:': 'Dujinis', 'Įrengimas:': 'Įrengtas', 'Nuoroda': 'www.aruodas.lt/1-3242301', 'Įdėtas': '2022-10-13', 'Redaguotas': '2022-10-13', 'Įsiminė': ['26'], 'Peržiūrėjo': '626/83 (iš viso/šiandien)', 'kaina_eur': 165000, 'coordinate_x': 54.864901, 'coordinate_y': 23.91818, 'Skelbimą peržiūrėjo (iš viso/šiandien)': ['626/83'], 'Skelbimo tekstas': 'PARDUODAMAS 3-JŲ KAMBARIŲ BUTAS PUIKIOJE VIETOJE FREDOJE!Parduodamas tvarkingas 3-jų kambarių butas Fredoje. Butui priklauso sandėliukas ir parkavimo vieta požeminiame parkinge! Kiemas naujai išklotas trinkelėmis iki pat pagrindinės gatvės, geras privažiavimas, rami vieta. Butas yra šiltas ir šviesus, nedideli šildymo mokesčiai žiemą. Aukšte yra tik vienas butas, visoje laiptinėje tik trys butai!\n-----------------------------\nPRIVALUMAI:\n- Šildomos grindys;\n- Nerasoja langai prie radiatorių, nes po plytelėmis šildomos grindys;\n- Spintoje po plytelėmis šildomos grindys;\n- Vidaus sienos - mūrinės;\n- Dujinis katilas yra ne momentinis, o su 50L talpa, tad visuomet yra paruoštas karštas vanduo;\n- Kieme iki pat asfaltuotos gatvės bus išklotos trinkelės (jau sumokėti pinigai);\n- Namo pirmininkas, kuris rūpinasi visais iškilusiais klausimais;\n- Butui priklauso sandėliukas;\n- Butui priklauso parkavimo vieta požeminiame parkinge;\n- Nedideli šildymo mokesčiai;\n- Tik vienas butas aukšte;\n- Aukštos lubos;\n- Butas nereikalauja jokių papildomų investicijų;\n- Rami vieta;\n- Išvystyti dviračių takai, kuriais galite pasiekti centrą ir visus kitus mikrorajonus dviračiu;\n- Oro tarša: labai žema (šalt. www.kurgyvenu.lt)\n-----------------------------\nBENDRA INFORMACIJA:\n- Statybos metai: 2012\n- Kambarių sk.: 3\n- Aukštas: 3/3\n- Plotas: 81.64 m²\n- Šildymas: dujinis\n-----------------------------\nATSTUMAI:\n~3.84 km. Atstumas iki centro\n~2.75 km. Kauno Autobusų stotis\n~2.46 km. Kauno keleivinė geležinkelio stotis\n-----------------------------\n• Jeigu norite sužinoti daugiau informacijos ar sutarti laiką apžiūrai, susisiekime Jums patogiu metu!\n• Galiu padėti gauti finansavimą šiam būstui įsigyti!\n• Esant poreikiui galiu parduoti ir Jūsų turtą!', 'error_get_energy_consumption_class': "'NoneType' object has no attribute 'text'", 'Azoto dioksidas (NO2)': '10.3 µg/m3', 'Kietosios dalelės (KD10)': '30.2 µg/m3', 'url_crawl': 'https://www.aruodas.lt/butai-kaune-fredoje-t-ivanausko-g-parduodamas-3-ju-kambariu-butas-puikioje-1-3242301/'}
#
# main_list=[dict_0,dict_1, dict_2]
# print(pd.DataFrame(main_list))
# exit()
def print_all_dfs(obj):
    print(obj.main_data)
    print(obj.crime)
    print(obj.surroundings)

class driver_4_bs4:
    def __init__(self, page_source, current_url):
        self.page_source = page_source
        self.current_url = current_url

def make_driver_from_html(url):
    with open(f'other/html/{url}', 'r', encoding='utf-8') as pg_src:
        pg_src=pg_src.read()
    driver = driver_4_bs4(page_source=pg_src, current_url=url)
    return driver

tipas='butu-nuoma'
crawl_date_yyyy_mm_dd = '2022_10_24'
url_list = os.listdir("other/html")

all_scr_data = sc.scraped_data(main_data=[], crime=[], surroundings=[])
for url in url_list:
    driver = make_driver_from_html(url)

    try:
        url_page_data = sc.scraped_data(main_data=None, crime=None, surroundings=None)
        url_page_data.scrape_data(driver)

        all_scr_data.update_with_scraped_data(url_page_data)
    except InvalidIndexError:
        print(f'Failed to scrape this URL: {url}')
        all_scr_data.to_df().clean_df()
        all_scr_data.add_scrape_date()
        all_scr_data.save_all_csv(all_scr_data, 'data/temporal', crawl_date_yyyy_mm_dd)

all_scr_data.to_df().clean_df()
all_scr_data.add_scrape_date()
all_scr_data.save_all_csv('data/temporal', crawl_date_yyyy_mm_dd)

os.makedirs(f"data/{tipas}/{crawl_date_yyyy_mm_dd}", exist_ok=True)

all_scr_data.save_all_xlsx(tipas, crawl_date_yyyy_mm_dd)
all_scr_data.save_main_csv(tipas, crawl_date_yyyy_mm_dd)



# print_all_dfs(all_scr_data)

'''
pandas to dict
'''
# crawl_date_yyyy_mm_dd = '2022_10_12'

# driver = sc.get_driver()
# scr_page_data = sc.scraped_data(main_data=None, crime=None, surroundings=None)

# for url in url_list:
    # sc.enter_url(url, driver)
    # upd_scr_page_data = scr_page_data.scrape_data(driver)

    # scr_page_data = scr_page_data.update_with_scraped_data(upd_scr_page_data)
# driver.quit()
# print(pd.DataFrame(scr_page_data.main_data))

exit()
# test df -> dict
crawl_date_yyyy_mm_dd = '2022_10_12'
data = sc.scraped_data(None, None, None).make_from_temp_folder(crawl_date_yyyy_mm_dd)
type = 'index'
dic_crime = data.crime.to_dict(type)
dic_surroundings = data.surroundings.to_dict(type)
dic_crime_2 = data.crime.to_dict(type)
data_dict = [*dic_crime.values()] + [*dic_surroundings.values()]
df_all = pd.DataFrame.from_dict(data_dict, orient='columns')
print(data_dict)
print(df_all)

# print(df.head())
# print(df.shape)

# test obf -> dict
exit()
'''
asynco
'''
import aiohttp
import asyncio
import regex as re
import time
import scraper.aruodas_lib_2.scraper as sc


def get_links():
    crawl_date_yyyy_mm_dd = '2022_10_12'
    url_list = sc.get_raw_urls(crawl_date_yyyy_mm_dd, 'butu-nuoma')
    return url_list


async def get_response(session, url):
    async with session.get(url) as resp:
        text = await resp.text()

        exp = r'(<title>).*(<\/title>)'

        return re.search(exp, text, flags=re.DOTALL).group(0)


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:

        tasks = []

        for url in get_links():
            tasks.append(asyncio.create_task(get_response(session, url)))

        results = await asyncio.gather(*tasks)

        for result in results:
            print(result)

    print(f"{(time.time() - start_time):.2f} seconds")


# asyncio.run(main())

'''
proxy
'''

import requests
from itertools import cycle

# Enter proxy ip's and ports in a list.
proxies = {
    'http://129.226.33.104:3218',
    'http://169.57.1.85:8123',
    'http://85.25.91.141:15333',
    'http://103.149.162.195:80',
    'http://8.218.213.95:10809'
}

proxy_pool = cycle(proxies)
# Initialize a URL.
url = 'https://httpbin.org/ip'
# Iterate through the proxies and check if it is working.
for i in range(1, 6):
    # Get a proxy from the pool
    proxy = next(proxy_pool)
    print("Request #%d" % i)
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=30)
        print(response.json())
    except:
        # Most free proxies will often get connection errors. You will need to retry the request using another proxy.
        print("Skipping. Connection error")
