import requests
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
title = "ibge_pesquisas"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
url = "https://servicodados.ibge.gov.br/api/v1/pesquisas"

response = requests.get(url)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    
    rows = []
    for pesquisa in data:
        pesquisa_id = pesquisa.get('id') 
        nome_pesquisa = pesquisa.get('nome')
        descricao_pesquisa = pesquisa.get('nome')
        contexto = pesquisa.get('contexto')
        for periodo in pesquisa.get('periodos', []):
            row = {
                'ID Pesquisa': pesquisa_id,
                'Nome Pesquisa': nome_pesquisa,
                'Descricao Pesquisa': descricao_pesquisa,
                'Contexto': contexto,
                'Periodo': periodo.get('periodo'),
                'Fonte': ', '.join(periodo.get('fonte', [])),
                'Publicacao': periodo.get('publicacao'),
                'Versao': periodo.get('versao')
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    save_dataframe_to_csv(df, save_path, layer, title, datetime_now)
else:
    print(f"Erro na requisição: {response.status_code}")