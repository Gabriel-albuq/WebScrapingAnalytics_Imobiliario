import requests
import json
import pandas as pd
import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.save_dataframe_csv import save_dataframe_to_csv

# Inputs
save_path = r'data\outputs'
layer = 'bronze'
title = "ibge_pib_municipios"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
url = "https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/2021/variaveis/37?localidades=N6[all]"

response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    
    # Extração e transformação dos dados
    results = []
    
    # Navega na estrutura JSON e extrai as informações
    for result in data:
        for item in result['resultados']:
            for serie in item['series']:
                for year, value in serie['serie'].items():
                    localidade_nome = serie['localidade']['nome']
                    localidade_id = serie['localidade']['id']
                    nivel_id = serie['localidade']['nivel']['id']
                    nivel_nome = serie['localidade']['nivel']['nome']
                    year_value = year
                    valor = value
                    results.append({
                        'id_localidade': localidade_id,
                        'nome_localidade': localidade_nome,
                        'id_nivel': nivel_id,
                        'nome_nivel': nivel_nome,
                        'ano': year_value,
                        'valor': valor
                    })
    
    # Criando o DataFrame
    df = pd.DataFrame(results)

    # Salvar em CSV
    save_dataframe_to_csv(df, save_path, layer, title, datetime_now)
else:
    print(f"Erro na requisição: {response.status_code}")
