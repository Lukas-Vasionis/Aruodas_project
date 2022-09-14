from bs4 import BeautifulSoup
import regex as re
import pandas as pd
import sys


# """## **Skelbimo pavadinimas**""")

def get_skelbimo_pavadinimas(soup):
    try:
        skelbimo_pavadinimas = re.sub('\s{2,}', '', soup.find_all(class_="obj-header-text")[0].get_text())
        skelbimo_pavadinimas = pd.DataFrame({'skelbimo_pavadinimas': [skelbimo_pavadinimas]})
        return (skelbimo_pavadinimas)
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


def get_tbl_obj_details_v2(soup, class_name):
    """
        ## **Skelbimo datos**
        ## **Pagrindinė lentelė**


    # ## **Pagrindinė lentelė**
    Naudoti obj-stats klasę:  get_tbl_obj_details_v2(soup, "obj-stats")

    # ## **Skelbimo datos**)
    Naudoti obj-details klasę: get_tbl_obj_details_v2(soup, 'obj-details')
    """

    def strip_strings_v2(ls):

        ls = [x.replace(r"\s{2,}", '').replace("'", "").strip("\n").replace('\n', ', ').strip(', ') for x in ls]
        ls = [re.sub('(\s){2,}', '', x) for x in ls]
        return ls

    try:
        class_name = fr'{class_name}'

        regex = re.compile(f'.*{class_name}.*')

        soup_dl = soup.find_all(class_=regex)[0]

        dts = [x.get_text() for x in soup_dl.find_all('dt')]
        dds = [x.get_text() for x in soup_dl.find_all('dd')]

        dts = strip_strings_v2(dts)
        dds = strip_strings_v2(dds)

        df = pd.DataFrame(data={'parametras': dts, 'reiksmes': dds})
        df = df.loc[df['reiksmes'] != 'None', :]
        df = df.loc[~df['parametras'].str.contains('Reklama')]

        df = df.set_index(df.columns[0]).transpose()
        df = df.reset_index(drop=True)
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


# """## **Artimiausios įstaigos**""")
def get_df_artimiausios_istaigos(soup):
    '''
    Reik sugalvot kaip patalpinti output - ar kaip nors į vieną eilutę,
    ar kurt db
    '''

    static_info_rows = soup.find(id="advertStatisticHolder").find_all(class_="statistic-info-row")

    def get_row_istaigu_tipas(row):

        def strip_strings_v2(ls):
            ls = [x.replace(r"\s{2,}", '').replace("'", "").strip("\n").replace('\n', ', ').strip(', ') for x in ls]
            ls = [re.sub('(\s){2,}', '', x) for x in ls]
            return ls

        # galima sutrumpint iki paieškos "  class_="cell-text"  "
        row_main_cell = row.find(class_="statistic-info-cell-main")
        if row_main_cell != None:
            row_main_cell = [x.string for x in row_main_cell if type(x) != 'str']

            row_main_cell = [x for x in row_main_cell if x != None]
            row_main_cell = strip_strings_v2(row_main_cell)
            row_main_cell = [x for x in row_main_cell if x != '']
            row_main_cell = [x for x in row_main_cell if not re.match('.*[0-9]+.*', x)]
            row_main_cell = " ".join([x for x in row_main_cell if x != ''])
            return row_main_cell

    def get_df_row_istaigos(row):
        row_detail_data = row.table
        if row_detail_data != None:
            df = pd.read_html(str(row_detail_data), flavor="bs4")[0]
            df.columns = ['atstumas_km', 'istaiga']
            df[['atstumas_km', 'matavimo_vnt']] = df.atstumas_km.str.replace('~', '').str.replace(',',
                                                                                                  '.').str.strip().str.split(
                ' ', expand=True)
            df.atstumas_km = df.atstumas_km.astype('float64')
            df.loc[df.matavimo_vnt == 'm', 'atstumas_km'] = df.loc[df.matavimo_vnt == 'm', 'atstumas_km'] / 1000
            df = df.drop('matavimo_vnt', axis=1)
            return df
        else:
            None

    def make_row_df(row_istaigu_tipas, df_row_istaigos):
        if row_istaigu_tipas != None or df_row_istaigos != None:
            df_row_istaigos.loc[:, 'istaigos_tipas'] = row_istaigu_tipas
            return (df_row_istaigos)

    df_all_rows = []
    for row in static_info_rows:
        row_istaigu_tipas = get_row_istaigu_tipas(row)
        df_row_istaigos = get_df_row_istaigos(row)
        df_row = make_row_df(row_istaigu_tipas, df_row_istaigos)

        df_all_rows.append(df_row)

    df_all_rows = pd.concat(df_all_rows).reset_index(drop=True)
    return (df_all_rows)

    # """## **Crime chart**"""


def get_crime_chart_data(soup):
    '''
    Reik sugalvot kaip patalpinti output - ar kaip nors į vieną eilutę,
    ar kurt db

    Taipogi reik sugalvot efektyvų būdą konvertuoti periodas+mėn į datą
    '''

    def get_crime_chart_period(soup):
        crime_chart_period = soup.find(id="advertStatisticHolder").find_all(class_="stat-chart-info")
        crime_chart_period = [x for x in crime_chart_period if 'Nusikal' in x.get_text()][0]

        crime_chart_period = re.sub('\)|\n|\s{2,}', '', crime_chart_period.get_text()).split('(')
        crime_chart_period = [x for x in crime_chart_period if x.startswith('2')][0]

        return crime_chart_period

    crime_chart_period = get_crime_chart_period(soup)
    soup_chart_div_crime = soup.find(id="advertStatisticHolder").find(id="chart_div_crime").table
    df = pd.read_html(str(soup_chart_div_crime), flavor="bs4")[0]

    df.columns = [f'Nusikaltimai {x}' if x != 'Mėn.' else x for x in df.columns]

    df.loc[:, 'periodas'] = crime_chart_period

    return (df)


# """## **Kaina**""")
def get_price_eur(soup):
    try:
        price_eur = soup.find_all(class_='price-eur')[0]
        price_eur = int(re.sub('[\n|\s\|€]+', '', price_eur.text))
        df = pd.DataFrame([price_eur], columns=['kaina_eur'])
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


# """## **Koordinatės**""")
def get_coordinates(soup):
    try:
        coordinates_href = soup.find_all(class_="link-obj-thumb vector-thumb-map")[0]['href']
        coordinates = coordinates_href.split('query=')[1].split('%2C')
        coordinates = [float(x) for x in coordinates]
        df = pd.DataFrame([coordinates], columns=['coordinate_x', 'coordinate_y'])
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


# """## **Skelbimo lanomumas**""")
def get_perziuru_sk(soup):
    try:
        skelbimo_perziura = soup.find_all(class_="obj-top-stats")[0].get_text().split('\n')
        skelbimo_perziura = [re.sub('\n+|(\s{2,})|\.', '', x) for x in skelbimo_perziura if x != '']
        skelbimo_perziura = [x.split(': ') for x in skelbimo_perziura]
        skelbimo_perziura = {k[0]: k[1:] for k in skelbimo_perziura}

        df = pd.DataFrame.from_dict(skelbimo_perziura)
        df = df.drop(['Įsiminė'], axis=1)
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


# """## **Skelbimo tekstas**""")
def get_skelbimo_tekstas(soup):
    try:
        skelbimo_tekstas = soup.find_all(id="collapsedText")[0].get_text()
        skelbimo_tekstas = re.sub('\s{2,}', '', skelbimo_tekstas)
        df = pd.DataFrame([skelbimo_tekstas], columns=['Skelbimo tekstas'])
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


def get_energy_consumption_class(soup):
    try:
        e_klase = soup.find(class_=re.compile('.*ec-current.*')).text
        e_klase = re.sub('\n+|(\s{2,})|\.', '', e_klase).strip()
        df = pd.DataFrame([e_klase], columns=['energijos_suvartojimo_klase'])
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df


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

        df = pd.DataFrame([col_values], columns=col_names)
    except Exception as error:
        df = pd.DataFrame([error], columns=[f'error_{sys._getframe().f_code.co_name}'])
    return df
