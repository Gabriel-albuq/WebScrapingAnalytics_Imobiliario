import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.save_dataframe_postgres import create_connection, create_table, save_to_database


table = 'ibge_municipios'
conn = create_connection()
create_municipios_query = f"""
CREATE TABLE IF NOT EXISTS {table} (
    uf VARCHAR(2),
    nome_uf VARCHAR(100),
    regiao_geografica_intermediaria VARCHAR(100),
    nome_regiao_geografica_intermediaria VARCHAR(100),
    regiao_geografica_imediata VARCHAR(100),
    nome_regiao_geografica_imediata VARCHAR(100),
    municipio VARCHAR(100),
    codigo_municipio_completo INTEGER,
    nome_municipio VARCHAR(100),
    PRIMARY KEY (codigo_municipio_completo)
);
"""
create_table(conn, create_municipios_query)

csv_path = r'data\outputs\ibge_municipios\bronze\2025-03-21_00-43-18\ibge_municipios-2025-03-21_00-43-18.csv'       
df = pd.read_csv(csv_path, encoding='utf-8').drop_duplicates()
save_to_database(df, table)

