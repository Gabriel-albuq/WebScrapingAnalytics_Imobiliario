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
title = "ibge01_municipios"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    results = []
    for municipio in data:
        results.append({
            "id": municipio["id"],
            "nome": municipio["nome"],
            "microrregiao_id": municipio["microrregiao"]["id"],
            "microrregiao_nome": municipio["microrregiao"]["nome"],
            "mesorregiao_id": municipio["microrregiao"]["mesorregiao"]["id"],
            "mesorregiao_nome": municipio["microrregiao"]["mesorregiao"]["nome"],
            "uf_id": municipio["microrregiao"]["mesorregiao"]["UF"]["id"],
            "uf_sigla": municipio["microrregiao"]["mesorregiao"]["UF"]["sigla"],
            "uf_nome": municipio["microrregiao"]["mesorregiao"]["UF"]["nome"],
            "regiao_id": municipio["microrregiao"]["mesorregiao"]["UF"]["regiao"]["id"],
            "regiao_sigla": municipio["microrregiao"]["mesorregiao"]["UF"]["regiao"]["sigla"],
            "regiao_nome": municipio["microrregiao"]["mesorregiao"]["UF"]["regiao"]["nome"]
        })

    df = pd.DataFrame(results)
    df['nome'] = df['nome'].apply(lambda x: unidecode(str(x)))
    df['microrregiao_nome'] = df['microrregiao_nome'].apply(lambda x: unidecode(str(x)))
    df['mesorregiao_nome'] = df['mesorregiao_nome'].apply(lambda x: unidecode(str(x)))
    df['uf_sigla'] = df['uf_sigla'].apply(lambda x: unidecode(str(x)))
    df['uf_nome'] = df['uf_nome'].apply(lambda x: unidecode(str(x)))
    df['regiao_sigla'] = df['regiao_sigla'].apply(lambda x: unidecode(str(x)))
    df['regiao_nome'] = df['regiao_nome'].apply(lambda x: unidecode(str(x)))

    print(df.head())

    save_response_to_json(data, save_path, "bronze", title, datetime_now)
    save_dataframe_to_csv(df, save_path, "silver", title, datetime_now)

else:
    print(f"Erro ao acessar API: {response.status_code}")
