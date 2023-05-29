from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import sys


# """## **Skelbimo pavadinimas**""")

def get_skelbimo_pavadinimas(soup):
    try:
        # Scraping and trimming the Ad's name
        skelbimo_pavadinimas = soup.find_all(class_="obj-header-text")[0].get_text()
        skelbimo_pavadinimas = re.sub('\s{2,}', '',skelbimo_pavadinimas)
        skelbimo_pavadinimas = {'skelbimo_pavadinimas': skelbimo_pavadinimas}
    except Exception as error:
        skelbimo_pavadinimas = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return skelbimo_pavadinimas


def get_tbl_obj_details_v2(soup, class_name):
    """
    Scrapes on of two tables in the page

    :param soup: bs4 object
    :param class_name: Possible values - "obj-details" or "obj-stats" - to choose which data table to scrape (see page source)
    :return: dict of page elements "obj-details" or "obj-stats"
    """

    def strip_strings_v2(ls):

        ls = [x.replace(r"\s{2,}", '').replace("'", "").strip("\n").replace('\n', ', ').strip(', ') for x in ls]
        ls = [re.sub('(\s){2,}', '', x) for x in ls]
        return ls

    try:
        # In case the class name changes, a regex pattern is created
        class_name = fr'{class_name}'
        regex = re.compile(f'.*{class_name}.*')

        # Finding the choosen html object
        soup_dl = soup.find_all(class_=regex)[0]

        # Converting its columns into key value pairs {dts:dds}
        dts = [x.get_text() for x in soup_dl.find_all('dt')]
        dds = [x.get_text() for x in soup_dl.find_all('dd')]

        dts = strip_strings_v2(dts)
        dds = strip_strings_v2(dds)

        data = dict(zip(dts, dds))

        # Discarding the rubish
        data = {key: value for (key, value) in data.items() if value != 'None' if 'Reklama' not in key}

    except Exception as error:
        # In case element is not found, the error is stored into the data
        data = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return data


# """## **Artimiausios įstaigos**""")
def get_df_artimiausios_istaigos(soup):
    '''
    Reik sugalvot kaip patalpinti output - ar kaip nors į vieną eilutę,
    ar kurt db
    '''

    def get_row_istaigu_tipas(row):

        def strip_strings_v2(ls):
            ls = [x.replace(r"\s{2,}", '').replace("'", "").strip("\n").replace('\n', ', ').strip(', ') for x in ls]
            ls = [re.sub('(\s){2,}', '', x) for x in ls]
            return ls

        # galima sutrumpint iki paieškos "  class_="cell-text"  "
        row_main_cell = row.find(class_="statistic-info-cell-main")
        if row_main_cell != None:
            row_main_cell = [x.string for x in row_main_cell if type(x) != 'str']
            row_main_cell = [x for x in row_main_cell if x is not None]

            row_main_cell = strip_strings_v2(row_main_cell)
            row_main_cell = [x for x in row_main_cell if x != '' if not re.match('.*[0-9]+.*', x)]
            row_main_cell = " ".join([x for x in row_main_cell if x != ''])
            return row_main_cell

    def get_df_row_istaigos(row):
        row_detail_data = row.table
        if row_detail_data is not None:

            surroundings = [row.findAll('td') for row in row_detail_data.findAll('tr')]
            surroundings = [x for x in surroundings if len(x) != 0]
            surroundings = [[x.text for x in td] for td in surroundings]
            surroundings = [[x.replace('\n', '') for x in td] for td in surroundings]
            surroundings = [td + [None] for td in surroundings]
            return surroundings
        else:
            None

    def make_data_row(row_istaigu_tipas, row_istaigos):
        if row_istaigu_tipas != None or row_istaigos != None:
            data_row = [[row_istaigu_tipas] + x for x in row_istaigos]

            return data_row

    try:
        static_info_rows = soup.find(id="advertStatisticHolder").find_all(class_="statistic-info-row")
        static_info_rows = [x for x in static_info_rows if x!=None]
        data_all_rows = []

        for row in static_info_rows:
            row_istaigu_tipas = get_row_istaigu_tipas(row)
            row_istaigos = get_df_row_istaigos(row)
            data_row = make_data_row(row_istaigu_tipas, row_istaigos)
            if data_row != None:
                data_all_rows = data_all_rows + data_row


        return data_all_rows
    except Exception as error:
        data_all_rows = [[None, None, error]]
        return data_all_rows

    # """## **Crime chart**"""


def get_crime_chart_data(soup):
    def get_crime_chart_period(soup):
        crime_chart_period = soup.find(id="advertStatisticHolder").find_all(class_="stat-chart-info")
        crime_chart_period = [x for x in crime_chart_period if 'Nusikal' in x.get_text()][0]

        crime_chart_period = re.sub('\)|\n|\s{2,}', '', crime_chart_period.get_text()).split('(')
        crime_chart_period = [x for x in crime_chart_period if x.startswith('2')][0]

        return crime_chart_period

    try:
        '''
        Reik sugalvot kaip patalpinti output - ar kaip nors į vieną eilutę,
        ar kurt db
    
        Taipogi reik sugalvot efektyvų būdą konvertuoti periodas+mėn į datą
        '''

        crime_chart_period = get_crime_chart_period(soup)
        soup_chart_div_crime = soup.find(id="advertStatisticHolder").find(id="chart_div_crime").table

        crimes = [row.findAll('td') for row in soup_chart_div_crime.findAll('tr')]
        crimes = [x for x in crimes if len(x) != 0]
        crimes = [[x.text for x in td] for td in crimes]
        crimes = [row + [crime_chart_period, None, None] for row in crimes]  # Adding crimechart period, error value and scrape_date values(none as there is no error in this case and date is yet to be marked)

        return crimes
    except Exception as error:
        crimes = [[None, None, None, error, None]]
    return crimes


# """## **Kaina**""")
def get_price_eur(soup):

    try:
        price_eur = soup.find_all(class_='price-eur')[0]
        price_eur = int(re.sub('[\n|\s\|€]+', '', price_eur.text))

        price_eur = {'kaina_eur': price_eur}
    except Exception as error:
        price_eur = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return price_eur


# """## **Koordinatės**""")
def get_coordinates(soup):
    try:
        coordinates_href = soup.find_all(class_="link-obj-thumb vector-thumb-map")[0]['href']
        coordinates = coordinates_href.split('query=')[1].split('%2C')
        coordinates = [float(x) for x in coordinates]
        coordinates = dict(zip(['coordinate_x', 'coordinate_y'], coordinates))
    except Exception as error:
        coordinates = {f'error_{sys._getframe().f_code.co_name}': str(error)}

    return coordinates


# """## **Skelbimo lanomumas**""")
def get_perziuru_sk(soup):
    try:
        skelbimo_perziura = soup.find_all(class_="obj-top-stats")[0].get_text().split('\n')
        skelbimo_perziura = [re.sub('\n+|(\s{2,})|\.', '', x) for x in skelbimo_perziura if x != '']
        skelbimo_perziura = [x.split(': ') for x in skelbimo_perziura]
        skelbimo_perziura = {k[0]: k[1:][0] for k in skelbimo_perziura}


    except Exception as error:
        skelbimo_perziura = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return skelbimo_perziura


# """## **Skelbimo tekstas**""")
def get_skelbimo_tekstas(soup):
    try:
        skelbimo_tekstas = soup.find_all(id="collapsedText")[0].get_text()
        skelbimo_tekstas = re.sub('\s{2,}', '', skelbimo_tekstas)
        skelbimo_tekstas = {'Skelbimo tekstas': skelbimo_tekstas}
    except Exception as error:
        skelbimo_tekstas = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return skelbimo_tekstas


def get_energy_consumption_class(soup):
    try:
        e_klase = soup.find(class_=re.compile('.*ec-current.*')).text
        e_klase = re.sub('\n+|(\s{2,})|\.', '', e_klase).strip()
        e_klase = {'energijos_suvartojimo_klase': e_klase}

    except Exception as error:
        e_klase = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return e_klase


def get_air_polution_data(soup):
    try:
        air = soup.find(class_='air-pollution__wrapper')
        air = air.find_all(class_='air-pollution__column')

        col_values = []
        col_names = []

        for i in air:
            val = i.div.span.text
            col = i.div.text.replace(val, '').strip()
            col_values.append(val)
            col_names.append(col)
        air = dict(zip(col_names, col_values))

    except Exception as error:
        air = {f'error_{sys._getframe().f_code.co_name}': str(error)}
    return air
