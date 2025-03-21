from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import pandas as pd
import sys
import os
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.browser_provider import BrowserProvider
from src.utils.functions_scrap import open_page, scroll_to_end, get_html, get_cards
from src.utils.save_dataframe_csv import save_dataframe_to_csv

# Inputs
driver_path = 'msedgedriver.exe'
save_path = r'data\outputs'
list_cities = ["ac+rio-branco", "al+maceio", "am+manaus", "ap+macapa", "ba+salvador", "ce+fortaleza", "df+brasilia", "es+vitoria", "go+goiania", "ma+sao-luis", 
               "mt+cuiaba", "ms+campo-grande", "mg+belo-horizonte", "pa+belem", "pb+joao-pessoa", "pr+curitiba", "pe+recife", "pi+teresina", "rj+rio-de-janeiro", 
               "rn+natal", "rs+porto-alegre", "ro+porto-velho", "rr+boa-vista", "sc+florianopolis", "sp+sao-paulo", "se+aracaju", "to+palmas"]

# Rodar os scripts para ir no site buscar cidade por cidade, página por página
element_list = "listing-wrapper__content"
element_card = ".//div[@data-position]"
element_error = "error-feedback"
element_empty = "result-empty"

datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
provider = BrowserProvider()
df = pd.DataFrame()
for city in list_cities:
    print(f"Buscar a cidade: {city}")
    continue_city = True
    i = 0
    while continue_city:
        i += 1
        browser = provider.get_browser(driver_path=driver_path)
        url = f"https://www.zapimoveis.com.br/lancamentos/imoveis/{city}/?areaMaxima=120&tipos=apartamento_residencial&pagina={i}"
        open_page(browser, url)

        return_scroll = scroll_to_end(browser, element_list, element_card, element_error, element_empty)

        if return_scroll:
            page_source, page_source_soup = get_html(browser)

            df_city_page = get_cards(city, page_source_soup, datetime_now)

            df= pd.concat([df, df_city_page], ignore_index=True)

        else:
            continue_city = False

        browser.quit()

layer = 'bronze'
title = "ZapImoveis"
save_dataframe_to_csv(df, save_path, layer, title, datetime_now)


