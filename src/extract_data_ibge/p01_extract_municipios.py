import pandas as pd
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.save_dataframe_csv import save_dataframe_to_csv

# Inputs
save_path = r'data\outputs'
layer = 'bronze'
title = "ibge_municipios"
datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

file_path = r'data\inputs\RELATORIO_DTB_BRASIL_MUNICIPIO.xlsx'
df = pd.read_excel(file_path, skiprows=6, engine='openpyxl')
df.columns = [
    'uf',
    'nome_uf',
    'regiao_geografica_intermediaria',
    'nome_regiao_geografica_intermediaria',
    'regiao_geografica_imediata',
    'nome_regiao_geografica_imediata',
    'municipio',
    'codigo_municipio_completo',
    'nome_municipio'
]
save_dataframe_to_csv(df, save_path, layer, title, datetime_now)

