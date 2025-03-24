import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.layer02_silver_postgres.utils.p00_update_agregados_municipios_2022_postgres import update_ibge00_agregados_municipios_2022
from src.layer02_silver_postgres.utils.p01_update_municipios_postgres import update_ibge01_municipios
from src.layer02_silver_postgres.utils.p02_update_pib_postgres import update_ibge02_pib
from src.layer02_silver_postgres.utils.p03_update_populacao_territorio_postgres import update_ibge03_populacao_territorio
from src.layer02_silver_postgres.utils.p04_update_empregos import update_ibge04_empregos
from src.layer02_silver_postgres.utils.p05_update_ensino_superior import update_ibge05_ensino_superior
from src.layer02_silver_postgres.utils.p06_update_imoveis_postgres import update_zapimoveis

if __name__ == "__main__":
    layer = "silver"
    csv_path = r'data\outputs\ibge00_agregados_municipios_2022\silver\2025-03-23_21-52-33\ibge00_agregados_municipios_2022-2025-03-23_21-52-33.csv'
    update_ibge00_agregados_municipios_2022(csv_path, layer)

    csv_path = r'data\outputs\ibge01_municipios\silver\2025-03-23_21-52-37\ibge01_municipios-2025-03-23_21-52-37.csv'
    update_ibge01_municipios(csv_path, layer)

    csv_path = r'data\outputs\ibge02_pib\silver\2025-03-23_21-52-42\ibge02_pib-2025-03-23_21-52-42.csv'
    update_ibge02_pib(csv_path, layer)

    csv_path = r'data\outputs\ibge03_populacao_territorio\silver\2025-03-23_21-53-18\ibge03_populacao_territorio-2025-03-23_21-53-18.csv'
    update_ibge03_populacao_territorio(csv_path, layer)

    csv_path = r'data\outputs\ibge04_empregos\silver\2025-03-23_21-55-18\ibge04_empregos-2025-03-23_21-55-18.csv'
    update_ibge04_empregos(csv_path, layer)

    csv_path = r'data\outputs\ibge05_ensino_superior\silver\2025-03-23_21-58-59\ibge05_ensino_superior-2025-03-23_21-58-59.csv'
    update_ibge05_ensino_superior(csv_path, layer)

    csv_path = r'data\outputs\ZapImoveis\silver\2025-03-22_14-01-01\ZapImoveis-2025-03-22_14-01-01.csv'    
    update_zapimoveis(csv_path, layer)