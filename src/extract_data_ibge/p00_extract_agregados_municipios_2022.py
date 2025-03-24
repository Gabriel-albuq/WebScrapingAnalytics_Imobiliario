import requests
import time
import pandas as pd
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from utils.save01_response_json import save_response_to_json
from utils.save02_dataframe_csv import save_dataframe_to_csv

# Inputs
save_path = r'data\outputs'
title = "ibge00_agregados_municipios_2022"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
url_agregados = "https://servicodados.ibge.gov.br/api/v3/agregados?nivel=N6&periodo=2020"


response = requests.get(url_agregados)
if response.status_code == 200:
    data = response.json()
    results = []
    for idx_categoria, categoria in enumerate(data, 1):
        id_categoria = categoria['id']
        nome_categoria = categoria['nome']

        for agregado in categoria.get('agregados', []):
            id_agregado = agregado['id']
            nome_agregado = agregado['nome']

            # Adicionando cada agregado na lista
            results.append({
                'Categoria_ID': id_categoria,
                'Categoria_Nome': nome_categoria,
                'Agregado_ID': id_agregado,
                'Agregado_Nome': nome_agregado
            })

    df = pd.DataFrame(results)
    print(df.head())

    save_response_to_json(data, save_path, "bronze", title, datetime_now)
    save_dataframe_to_csv(df, save_path, "silver", title, datetime_now)

else:
    print(f"Erro ao acessar API: {response.status_code}")

