

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

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.browser_provider import BrowserProvider

def open_page(browser, url):
    """
    Script para acessar a página.

    :param browser: Browser usado para abrir as páginas.
    :param url: Url da página a ser visitada.
    """
    try:
        # Abrindo a página desejada
        browser.get(url)

    except:
        print("Falha ao acessar a página")

def scroll_to_end(browser, element_list, element_card, element_error, element_empty):
    """
    Script para ir até o último elemento da lista, até não ter mais elementos. 
    Em caso de páginas que abre mais itens com o scroll, esse script serve para ir abrindo os itens.

    :param browser: Browser usado para abrir as páginas.
    :param element_list: Elemento da lista onde estão os itens.
    :param element_card: Elemento dos itens da lista.
    :param element_error: Elemento para quando o site não existe.
    :param element_empty: Elemento para quando a lista estiver vazia.

    :return: True caso tenha itens, False caso esteja vazia.
    """
    try:
        att = True
        last_element = None
        limit = 60
        count = 0
        while att:
            count += 1
            # Verificar primeiro se encontra o elemento que indica que a página existe
            try:
                result_error = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, element_error))
                )
            
                if result_error:
                    print("O site não existe.")
                    return False
            except TimeoutException:
                pass

            # Verificar depois se encontra o elemento que indica que a lista está vazia
            try:
                result_empty = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, element_empty))
                )
            
                if result_empty:
                    print("Nenhum resultado encontrado.")
                    return False
            except TimeoutException:
                pass

            # Verificar depois se encontra a lista
            try: 
                wrapper = WebDriverWait(browser, 1).until(
                    EC.presence_of_element_located((By.CLASS_NAME, element_list))
                )

                elements = wrapper.find_elements(By.XPATH, element_card)

                if elements and last_element:
                    if last_element == elements[-1]:
                        return True
                        
                    else:
                        last_element = elements[-1]
                        browser.execute_script("arguments[0].scrollIntoView();", last_element)
                        time.sleep(5)

                else:
                    last_element = elements[-1]
                    browser.execute_script("arguments[0].scrollIntoView();", last_element)
                    time.sleep(5)
            
            except TimeoutException:
                if count >= limit:
                    return False

    except Exception as e:
        print(f"Erro: {e}")

def get_html(browser):
    """
    Script para pegar o conteúdo da página
    
    :param browser: Browser usado para abrir as páginas.

    :return: Retorna o conteúdo da página e a versão dele no BeautifulSoup.
    """
    page_source = browser.page_source
    page_source_soup = BeautifulSoup(page_source, 'html.parser')

    return page_source, page_source_soup

def get_cards(city, page_source_soup, datetime_now):
    """
    Script para pegar os elementos de interesse que estão presentes no HTML

    :param city: Cidade em que foi obtido o HTML.
    :param page_source_soup: HTML da página o BeautifulSoup.

    :return: Retorna o Dataframe caso tenha itens, e None caso não tenha nada.
    """
    # Listas para armazenar os dados
    list_property_id = []
    list_city = []
    list_locations = []
    list_streets = []
    list_type_realese = []
    list_areas = []
    list_rooms = []
    list_bathrooms = []
    list_price = []
    list_links = []
    list_datetime = []

    listing_wrapper_content = page_source_soup.find('div', class_='listing-wrapper__content')
    if listing_wrapper_content:
        listing_card_result = listing_wrapper_content.find_all('div', class_='ListingCard_result-card__Pumtx')
        for card_result in listing_card_result:
            try:
                # Extraindo o data-id do link
                property_id = card_result.find('a', {'itemprop': 'url'}).get('data-id')
            except:
                property_id = None

            try:
                location = card_result.find('span', {'data-cy': 'rp-cardProperty-location-txt'}).text
            except:
                location = None

            try:
                street = card_result.find('p', {'data-cy': 'rp-cardProperty-street-txt'}).text
            except:
                street = None

            try:
                type_realese = card_result.find('div', {'class': 'l-tag-card__content'}).text
            except:
                type_realese = None

            try:
                area = card_result.find('li', {'data-cy': 'rp-cardProperty-propertyArea-txt'}).text
            except:
                area = None

            try:
                rooms = card_result.find('li', {'data-cy': 'rp-cardProperty-bedroomQuantity-txt'}).text
            except:
                rooms = None

            try:
                bathrooms = card_result.find('li', {'data-cy': 'rp-cardProperty-bathroomQuantity-txt'}).text
            except:
                bathrooms = None

            try:
                price = card_result.find('p', {'l-text l-u-color-neutral-28 l-text--variant-heading-small l-text--weight-bold undefined'}).text
            except:
                price = None

            try:
                link = card_result.find('a', {'itemprop': 'url'})['href']
            except:
                link = None

            # Adicionar os dados às listas
            list_property_id.append(property_id)
            list_city.append(city)
            list_locations.append(location)
            list_streets.append(street)
            list_type_realese.append(type_realese)
            list_areas.append(area)
            list_rooms.append(rooms)
            list_bathrooms.append(bathrooms)
            list_price.append(price)
            list_links.append(link) 
            list_datetime.append(datetime_now)       

        # Criar o DataFrame
        df = pd.DataFrame({
            'property_id': list_property_id,
            'state_city': list_city, 
            'location': list_locations,
            'street': list_streets,
            'type_realese': list_type_realese,
            'area': list_areas,
            'rooms': list_rooms,
            'bathrooms': list_bathrooms,
            'price': list_price,
            'link': list_links,
            'update_at': list_datetime
        })
    
        return df

    else:
        return None
