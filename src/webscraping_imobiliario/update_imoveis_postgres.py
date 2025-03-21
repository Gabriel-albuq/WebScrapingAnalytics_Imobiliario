import pandas as pd
import sys
import os
from unidecode import unidecode

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.save_dataframe_postgres import create_connection, create_table, save_to_database

table = 'imoveis_python'
conn = create_connection()

create_imoveis_query = f"""
CREATE TABLE IF NOT EXISTS {table} (
    property_id TEXT,
    state_city TEXT,
    location TEXT,
    street TEXT,
    type_realese TEXT,
    area TEXT,
    rooms TEXT,
    bathrooms TEXT,
    price TEXT,
    link TEXT,
    update_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (property_id, update_at)
);
"""
create_table(conn, create_imoveis_query)

csv_path = r'data\outputs\bronze\2025-03-20_20-38-27\ZapImoveis\ZapImoveis-2025-03-20_20-38-27.csv'       
df = pd.read_csv(csv_path, encoding='utf-8').drop_duplicates()
df['update_at'] = pd.to_datetime(df['update_at'], format='%Y-%m-%d_%H-%M-%S')
save_to_database(df, table)
