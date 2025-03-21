import time
import sys
import os
import pandas as pd
import ctypes
from datetime import datetime

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from .utils.key_mapping import map_key
from .utils.locator_mapping import map_locator
from .utils.verify_downloads import verify_downloads
# python -m src.tools.actions

DEFAULT_SLEEP = 1

def goto(name, browser, name_step, att, log_file):
    link = att['link']
    tentativa = 0
    num_try = 1200
    
    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP
    time.sleep(sleep)

    with open(log_file, 'a', encoding='utf-8') as log_file:
        date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
        print(f"\n({date_hour_now}) {name} - {name_step}", end="")

        while tentativa <= num_try:
            try:
                browser.get(link)
                
                log_file.write("OK")
                print("OK")

                break
            except Exception as e:
                log_file.write(".")
                #print(".", end="")
                tentativa += 1
        
        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def find_element(name, browser, name_step, att, log_file):    
    num_try = 1200
    error_return ="400"
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']

    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait) # Cria uma instância do WebDriverWait com tempo máximo de espera
            element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path))) # Espera até o elemento estar presente no DOM e visível na página
            
            log_file.write("OK")
            log_file.flush()
            print("OK")

            break

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".", end="")
    
        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def click_element(name, browser, name_step, att, log_file):  
    num_try = 1200
    error_return ="400"
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']
    try:
        locator_type = map_locator(att['locator_type'])
    except:
        locator_type = By.XPATH
    
    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait) # Cria uma instância do WebDriverWait com tempo máximo de espera
            element = espera.until(EC.visibility_of_element_located((locator_type, element_path))) # Espera até o elemento estar presente no DOM e visível na página
            element.click() # Clica no elemento quando encontrado
            
            log_file.write("OK")
            log_file.flush()
            print("OK")

            break

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".", end="")
    
        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def click_list_element(name, browser, name_step, att, log_file):  
    num_try = 1200
    error_return = "400"
    tentativa = 0
    time_wait = 1
    list_element_path = att['list_element_path']
    
    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    
    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            for element_path in list_element_path:  # Iterando sobre a lista de paths
                espera = WebDriverWait(browser, time_wait)  # Cria uma instância do WebDriverWait
                try:
                    # Espera até o elemento estar presente no DOM e visível
                    element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path)))  
                    element.click()  # Clica no elemento quando encontrado
                    
                    log_file.write(f"OK")  # Escreve no log que encontrou o elemento
                    log_file.flush()
                    print(f"OK")
                    
                    break  # Sai do loop se um elemento for clicado
                except Exception as inner_e:
                    continue  # Se não encontrar o elemento, continua para o próximo path
                    
            break  # Se algum elemento foi clicado, sai do loop principal
            
        except Exception as e:
            log_file.write(".")
            log_file.flush()
            # print(".", end="")
    
        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def click_element_right(name, browser, name_step, att, log_file):  
    num_try = 1200
    error_return ="400"
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']
    
    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait) # Cria uma instância do WebDriverWait com tempo máximo de espera
            element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path))) # Espera até o elemento estar presente no DOM e visível na página
            acao = ActionChains(browser) 
            acao.context_click(element)
            acao.perform()
            element.click() # Clica no elemento quando encontrado
            
            log_file.write("OK")
            log_file.flush()
            print("OK")

            break

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".", end="")
    
        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def click_key_element(name, browser, name_step, att, log_file):    
    num_try = 1200
    error_return = "400"
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']
    key = map_key(att['key'])

    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait)  # Espera o elemento estar visível
            element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path)))  # Localiza o elemento
            element.send_keys(key)  # Clica no elemento
            
            log_file.write("OK")
            log_file.flush()
            print("OK")

            break

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".")
            tentativa += 1

        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def press_keys_sequence(name, browser, name_step, att, log_file):
    num_try = 1200
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']
    keys = [map_key(key) for key in att['keys']]  # Mapeia a lista de teclas recebida em att['keys']

    try:
        sleep = int(att['sleep'])
    except:
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")

    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait)  # Espera o elemento estar visível
            element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path)))  # Localiza o elemento

            actions = ActionChains(browser)
            # Pressiona e solta cada tecla da lista em sequência
            for key in keys:
                key = map_key(key)
                actions.key_down(key) # Pressionar

            for key in keys:
                key = map_key(key)
                actions.key_up(key) # Despressionar
            
            actions.perform()  # Executa toda a sequência de ações

            log_file.flush()
            print("OK")
            break

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".", end="")

        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def write_element(name, browser, name_step, att, log_file):
    num_try = 1200
    error_return = "400"
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']
    text = att['text']

    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP
               
    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa < num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait) # Cria uma instância do WebDriverWait com tempo máximo de espera
            element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path)))  # Espera até o elemento estar presente no DOM e visível na página
            element.clear()
            element.send_keys(text) # Escreve o texto no campo de entrada
            time.sleep(sleep)

            # Verifica se o texto foi escrito corretamente no elemento
            if element.get_attribute('value') == text:
                log_file.write("OK")
                log_file.flush()
                print("OK")
                break
            
            else:
                log_file.write(".")
                log_file.flush()

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".")

        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def write_list_element(name, browser, name_step, att, log_file):
    num_try = 1200
    tentativa = 0
    time_wait = 1
    list_element_path = att['list_element_path']
    text = att['text']
    
    try:
        sleep = int(att['sleep'])  
    except:
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d.%m.%Y")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa < num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait)

            for element_path in list_element_path:
                try:
                    element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path)))
                    element.clear()
                    element.send_keys(text)
                    time.sleep(sleep)

                    # Verifica se o texto foi escrito corretamente
                    if element.get_attribute('value') == text:
                        log_file.write("OK")
                        log_file.flush()
                        print("OK")
                        return  # Sai da função após encontrar e escrever no primeiro elemento disponível
                
                except Exception:
                    continue  # Se um elemento não for encontrado, tenta o próximo da lista
            
            log_file.write(".")
            log_file.flush()

        except Exception as e:
            log_file.write(".")
            log_file.flush()

        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}: {e}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}: {e}")

def verify_file_duplicate(name, browser, name_step, att, log_file):
    download_dir = att['download_dir']
    file_name = att['file_name']

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")

    try:
        # Lista todos os arquivos que contêm file_name no nome
        matching_files = [f for f in os.listdir(download_dir) if file_name in f]
        
        # Se houver arquivos correspondentes, excluí-los
        if matching_files:
            for file in matching_files:
                file_path = os.path.join(download_dir, file)
                os.remove(file_path)
                log_file.write(f"Arquivo removido: {file}\n")
                log_file.flush()
                print(f"Arquivo removido: {file}")
        else:
            log_file.write("Nenhum arquivo correspondente encontrado\n")
            log_file.flush()
            print("Nenhum arquivo correspondente encontrado")

        log_file.write("OK")
        log_file.flush()
        print("OK")

    except Exception as e:
        log_file.write(f"\n ########## Erro na {name_step}: {e}")
        log_file.flush()
        print(f"\n ########## Erro na {name_step}: {e}")

def verify_file_download(name, browser, name_step, att, log_file):
    download_dir = att['download_dir']
    file_name = att['file_name']
    
    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")

    try:
        if any(file_name in f for f in os.listdir(download_dir)):
            log_file.write("OK")
            log_file.flush()
            print("OK")
        else:
            raise FileNotFoundError("Arquivo não encontrado")

    except Exception as e:
        log_file.write(f"\n ########## Erro na {name_step}: {e}")
        log_file.flush()
        print(f"\n ########## Erro na {name_step}: {e}")

def agroup_data_mb51(name, browser, name_step, att, log_file):
    download_dir = att['download_dir']
    files_with_text = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if name in f]
    
    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    try:
        for file in files_with_text:
            df = pd.read_excel(file)
            df_grouped = df.groupby(
                ['Centro', 'Ordem', 'Material', 'Texto breve material', 'Depósito', 'Lote', 
                'Tipo de movimento', 'Data de lançamento', 'UM registro', 'UM básica', 
                'Data do documento', 'Nome do usuário', 'Data de entrada'], 
                as_index=False
            ).agg({'Quantidade': 'sum', 'Qtd.  UM registro': 'sum'})

            df_grouped.to_excel(file, index = False)

        log_file.write("OK")
        log_file.flush()
        print("OK")

    except Exception as e:
        log_file.write(f"\n ########## Erro na {name_step}: {e}")
        log_file.flush()
        print(f"\n ########## Erro na {name_step}: {e}")

def close_driver(name, browser, name_step, att, log_file):
    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >>")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    try:
        browser.quit()  # Fecha todas as janelas e encerra o WebDriver
        
        log_file.write("OK")
        log_file.flush()
        print("OK")

        date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"({date_hour_now}) {name} - OK")

    except Exception as e:
        log_file.write(f"\n ########## Erro na {name_step}: {e}")
        log_file.flush()
        print(f"\n ########## Erro na {name_step}: {e}")

def action_test(name, browser, name_step, att, log_file):  
    num_try = 1200
    error_return ="400"
    tentativa = 0
    time_wait = 1
    element_path = att['element_path']
    
    try:
        sleep = int(att['sleep'])  
    except:  
        sleep = DEFAULT_SLEEP

    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    while tentativa <= num_try:
        tentativa += 1
        try:
            time.sleep(sleep)
            espera = WebDriverWait(browser, time_wait) # Cria uma instância do WebDriverWait com tempo máximo de espera
            element = espera.until(EC.visibility_of_element_located((By.XPATH, element_path))) # Espera até o elemento estar presente no DOM e visível na página
            element.click() # Clica no elemento quando encontrado
            
            log_file.write("OK")
            log_file.flush()
            print("OK")

            break

        except Exception as e:
            log_file.write(".")
            log_file.flush()
            #print(".", end="")
    
        if tentativa == num_try:
            log_file.write(f"\n ########## Erro na {name_step}")
            log_file.flush()
            print(f"\n ########## Erro na {name_step}")
    time.sleep(100)

def focus_browser(browser):
    try:
        browser.switch_to.window(browser.current_window_handle)  # Alterna para a aba ativa
        print("Janela focada com sucesso.")
    except Exception as e:
        print(f"Erro ao focar a janela")

def generate_alert(name, browser, name_step, att, log_file):
    num_try = 1200
    error_return ="400"
    tentativa = 0
    time_wait = 1
    title = att['title']
    text = att['text']

    # date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    # log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    # log_file.flush()
    # print(f"\n({date_hour_now}) {name} - {name_step} >> ")
    ctypes.windll.user32.MessageBoxW(0, text, title, 0x40)

    # log_file.write("OK")
    # log_file.flush()

def rename_file(name, browser, name_step, att, log_file):
    download_dir = att['download_dir']
    file_name = att['file_name']
    new_file_name = att['new_file_name']
    
    if log_file:
        log_file = open(log_file, 'a', encoding='utf-8')
    else:
        log_file = None

    date_hour_now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    log_file.write(f"\n({date_hour_now}) {name} - {name_step} >> ")
    log_file.flush()
    print(f"\n({date_hour_now}) {name} - {name_step} >> ")

    try:
        # Procura um arquivo que contenha file_name no nome
        matching_files = [f for f in os.listdir(download_dir) if file_name in f]
        
        if matching_files:
            # Pega o primeiro arquivo encontrado
            old_file_path = os.path.join(download_dir, matching_files[0])
            new_file_path = os.path.join(download_dir, new_file_name)
            
            # Renomeia o arquivo
            os.rename(old_file_path, new_file_path)
            
            log_file.write(f"Arquivo renomeado: {matching_files[0]} -> {new_file_name}\n")
            log_file.flush()
            print(f"Arquivo renomeado: {matching_files[0]} -> {new_file_name}")
        else:
            log_file.write("Nenhum arquivo correspondente encontrado\n")
            log_file.flush()
            print("Nenhum arquivo correspondente encontrado")

    except Exception as e:
        log_file.write(f"\n ########## Erro na {name_step}: {e}")
        log_file.flush()
        print(f"\n ########## Erro na {name_step}: {e}")

action_dict = {}
action_dict['action_test'] = action_test
action_dict['goto'] = goto
action_dict['find_element'] = find_element
action_dict['click_element'] = click_element
action_dict['click_list_element'] = click_list_element
action_dict['click_element_right'] = click_element_right
action_dict['write_element'] = write_element
action_dict['write_list_element'] = write_list_element
action_dict['click_key_element'] = click_key_element
action_dict['press_keys_sequence'] = press_keys_sequence
action_dict['verify_file_duplicate'] = verify_file_duplicate
action_dict['verify_file_download'] = verify_file_download
action_dict['agroup_data_mb51'] = agroup_data_mb51
action_dict['close_driver'] = close_driver
action_dict['focus_browser'] = focus_browser
action_dict['generate_alert'] = generate_alert
action_dict["rename_file"] = rename_file