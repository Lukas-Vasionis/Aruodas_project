import time
import traceback

from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import aruodas_lib_2.utils_page_scraper as aruodas
import aruodas_lib_2.utils_pipeline

def get_photo_links(driver):

    """
    gets comma separated photo links into single value
    """

    try:
        time.sleep(1)
        soup = driver.page_source
        print(type(soup))
        pattern = r"https://aruodas-img\.dgn\.lt/object_[\w-]+/[\w-]+\.jpg"
        urls = re.findall(pattern, soup)
        # urls = [ x for x in urls if x not in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'webp', 'tiff', 'ico']]
        print(urls)
        print("shit")

        if len(urls) != 0:
            # if found  any - put it into dict
            urls = ",".join(urls)
            photos = {'photos': urls}
        else:
            # else put empty string
            urls = ""
            photos = {'photos': urls}

            print("No photo URL detected")
    except Exception as e:
        print(traceback.format_exc())
    return photos
pd.set_option('display.expand_frame_repr', False)


# with open('data/test.html', 'r', encoding='UTF-8') as html:
#     html=html.read()
#
# soup=BeautifulSoup(html, 'html.parser')

driver=aruodas_lib_2.utils_pipeline.get_driver(
    geckodriver_url="https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-win32.zip",
    geckodriver_folder="./",
    firefox_path='C:/Program Files/Mozilla Firefox/firefox.exe')

for u in [
    "https://www.aruodas.lt/butai-vilniuje-santariskese-dangerucio-g-jaukus-erdvus-uzdaras-ir-zalias-naujuju-1-3370060/",
    "https://www.aruodas.lt/butai-vilniuje-virsuliskese-virsilu-g-parduodama-be-tarpininku-tiesiai-is-1-3386240/",
    "https://www.aruodas.lt/butai-vilniuje-pasilaiciuose-sviliskiu-g-atviru-duru-dienos-nuo-sausio-d-iki-1-3394699/",
    "https://www.aruodas.lt/butai-vilniuje-pasilaiciuose-grigalaukio-g-atviru-duru-dienos-nuo-sausio-d-iki-1-3389637/"
]:
    print(u)
    time.sleep(1)
    aruodas_lib_2.utils_pipeline.enter_url(
        u,
        driver)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    get_photo_links(soup)



# skelbimo_pavadinimas = aruodas.get_skelbimo_pavadinimas(soup)
# df_skelbimo_santrauka = aruodas.get_tbl_obj_details_v2(soup, 'obj-details')
# df_skelbimo_datos = aruodas.get_tbl_obj_details_v2(soup, "obj-stats")
# price_eur = aruodas.get_price_eur(soup)
# coordinates = aruodas.get_coordinates(soup)
#
# skelbimo_perziura = aruodas.get_perziuru_sk(soup)
# skelbimo_tekstas = aruodas.get_skelbimo_tekstas(soup)
#
# e_klase=aruodas.get_energy_consumption_class(soup)
#
# oro_tarsa=aruodas.get_air_polution_data(soup)
# list_scraped_obj=[skelbimo_pavadinimas, price_eur, df_skelbimo_santrauka, df_skelbimo_datos,
#                  coordinates, skelbimo_perziura, e_klase, oro_tarsa, skelbimo_tekstas]
#
# # for i in list_scraped_obj:
# #     print(type(i))
# #     print(i.to_markdown())
# pd.concat(list_scraped_obj, axis=1).to_csv('scraped_del_me.csv', index=False)
exit()
