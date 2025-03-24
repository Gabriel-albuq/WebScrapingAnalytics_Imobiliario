import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

engine = create_engine_postgres(see_echo=False)

list_tables = ['silver.ibge00_agregados_municipios_2022', 'silver.ibge01_municipios', 'silver.ibge02_pib', 
               'silver.ibge03_populacao_territorio', 'silver.ibge04_empregos', 'silver.ibge05_ensino_superior']
for table in list_tables:
    query = f"SELECT * FROM {table} LIMIT 5"
    df = pd.read_sql(query, engine)

    print(table)
    print(df)
    print('\n')
