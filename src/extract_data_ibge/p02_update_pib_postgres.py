import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.save_dataframe_postgres import create_connection, create_table, save_to_database

table = 'ibge_pib_municipios'
conn = create_connection()
create_pib_municipios_query = f"""
CREATE TABLE IF NOT EXISTS {table} (
    id_localidade INTEGER,
    nome_localidade VARCHAR(255),
    id_nivel VARCHAR(10),
    nome_nivel VARCHAR(50),
    ano INTEGER,
    valor FLOAT,
    PRIMARY KEY (id_localidade, ano)
);
"""
create_table(conn, create_pib_municipios_query)

csv_path = r'data\outputs\ibge_pib_municipios\bronze\2025-03-21_00-49-40\ibge_pib_municipios-2025-03-21_00-49-40.csv'
df = pd.read_csv(csv_path, encoding='utf-8').drop_duplicates()
save_to_database(df, table)
