import requests
import json
import pandas as pd
import os
import sys
from datetime import datetime

# Adiciona o diretório raiz ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.save01_response_json import save_response_to_json
from utils.save02_dataframe_csv import save_dataframe_to_csv

# Inputs
save_path = r'data\outputs'
title = "ibge05_ensino_superior"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
url = "https://servicodados.ibge.gov.br/api/v3/agregados/10064/periodos/2022/variaveis/1920?localidades=N6[all]&classificacao=2082[78032]|58[95253]"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    results = []
    for result in data:
        for item in result['resultados']:
            for serie in item['series']:
                for year, value in serie['serie'].items():
                    results.append({
                        'id_pesquisa': result['id'],
                        'nome_pesquisa': result['variavel'],
                        'unidade': result['unidade'],
                        'id_nivel': serie['localidade']['nivel']['id'],
                        'nome_nivel': serie['localidade']['nivel']['nome'],
                        'id_localidade': serie['localidade']['id'],
                        'nome_localidade': serie['localidade']['nome'],
                        'serie': year,
                        'valor_serie': value
                    })

    df = pd.DataFrame(results)
    print(df.head())

    save_response_to_json(data, save_path, "bronze", title, datetime_now)
    save_dataframe_to_csv(df, save_path, "silver", title, datetime_now)
else:
    print(f"Erro na requisição: {response.status_code}")
