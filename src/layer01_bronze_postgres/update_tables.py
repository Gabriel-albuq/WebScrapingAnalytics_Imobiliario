import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.layer01_bronze_postgres.utils.p00_update_json_postgres import update_json_postgres


if __name__ == "__main__":
    layer = "bronze"

    table_name = 'ibge00_agregados_municipios_2022'
    csv_path = r'data\outputs\ibge00_agregados_municipios_2022\bronze\2025-03-23_21-52-33\ibge00_agregados_municipios_2022.json'
    update_json_postgres(table_name, csv_path, layer)

    table_name = 'ibge01_municipios'
    csv_path = r'data\outputs\ibge01_municipios\bronze\2025-03-23_21-52-37\ibge01_municipios.json'
    update_json_postgres(table_name, csv_path, layer)

    table_name = 'ibge02_pib'
    csv_path = r'data\outputs\ibge02_pib\bronze\2025-03-23_21-52-42\ibge02_pib.json'
    update_json_postgres(table_name, csv_path, layer)

    table_name = 'ibge03_populacao_territorio'
    csv_path = r'data\outputs\ibge03_populacao_territorio\bronze\2025-03-23_21-53-18\ibge03_populacao_territorio.json'
    update_json_postgres(table_name, csv_path, layer)

    table_name = 'ibge04_empregos'
    csv_path = r'data\outputs\ibge04_empregos\bronze\2025-03-23_21-55-18\ibge04_empregos.json'
    update_json_postgres(table_name, csv_path, layer)

    table_name = 'ibge05_ensino_superior'
    csv_path = r'data\outputs\ibge05_ensino_superior\bronze\2025-03-23_21-58-59\ibge05_ensino_superior.json'
    update_json_postgres(table_name, csv_path, layer)

    table_name = 'zapimoveis'  
    csv_path = r'data\outputs\ZapImoveis\bronze\2025-03-22_14-01-01\ZapImoveis.json'
    update_json_postgres(table_name, csv_path, layer)