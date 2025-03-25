import requests
import json
import pandas as pd
import os
import sys
from datetime import datetime
from unidecode import unidecode

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.save01_response_json import save_response_to_json
from utils.save02_dataframe_csv import save_dataframe_to_csv

# Inputs
save_path = r'data\outputs'
title = "ibge03_populacao_territorio"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
url = "https://servicodados.ibge.gov.br/api/v3/agregados/4714/periodos/2022/variaveis/93|6318|614?localidades=N6[all]"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    results = []
    for result in data:
            for item in result['resultados']:
                for serie in item['series']:
                    for year, value in serie['serie'].items():
                        localidade_nome = serie['localidade']['nome']
                        localidade_id = serie['localidade']['id']
                        nivel_id = serie['localidade']['nivel']['id']
                        nivel_nome = serie['localidade']['nivel']['nome']
                        variavel = result['variavel']
                        unidade = result['unidade']
                        nome_serie = year
                        valor_serie = value
                        results.append({
                            'id_pesquisa': result['id'],
                            'nome_pesquisa': variavel,
                            'unidade': unidade,
                            'id_nivel': nivel_id,
                            'nome_nivel': nivel_nome,
                            'id_localidade': localidade_id,
                            'nome_localidade': localidade_nome,
                            'serie': nome_serie,
                            'valor_serie': valor_serie
                        })

    df = pd.DataFrame(results)
    df['nome_pesquisa'] = df['nome_pesquisa'].apply(lambda x: unidecode(str(x)))
    df['unidade'] = df['unidade'].apply(lambda x: unidecode(str(x)))
    df['nome_nivel'] = df['nome_nivel'].apply(lambda x: unidecode(str(x)))
    df['nome_localidade'] = df['nome_localidade'].apply(lambda x: unidecode(str(x)))
    print(df.head())

    save_response_to_json(data, save_path, "bronze", title, datetime_now)
    save_dataframe_to_csv(df, save_path, "silver", title, datetime_now)
else:
    print(f"Erro na requisição: {response.status_code}")
