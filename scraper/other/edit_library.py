from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import aruodas_lib_2.get_tbl_library as aruodas


pd.set_option('display.expand_frame_repr', False)


with open('data/test.html', 'r', encoding='UTF-8') as html:
    html=html.read()
soup=BeautifulSoup(html, 'html.parser')

skelbimo_pavadinimas = aruodas.get_skelbimo_pavadinimas(soup)
df_skelbimo_santrauka = aruodas.get_tbl_obj_details_v2(soup, 'obj-details')
df_skelbimo_datos = aruodas.get_tbl_obj_details_v2(soup, "obj-stats")
price_eur = aruodas.get_price_eur(soup)
coordinates = aruodas.get_coordinates(soup)

skelbimo_perziura = aruodas.get_perziuru_sk(soup)
skelbimo_tekstas = aruodas.get_skelbimo_tekstas(soup)

e_klase=aruodas.get_energy_consumption_class(soup)

oro_tarsa=aruodas.get_air_polution_data(soup)
list_scraped_obj=[skelbimo_pavadinimas, price_eur, df_skelbimo_santrauka, df_skelbimo_datos,
                 coordinates, skelbimo_perziura, e_klase, oro_tarsa, skelbimo_tekstas]

# for i in list_scraped_obj:
#     print(type(i))
#     print(i.to_markdown())
pd.concat(list_scraped_obj, axis=1).to_csv('scraped_del_me.csv', index=False)
exit()
