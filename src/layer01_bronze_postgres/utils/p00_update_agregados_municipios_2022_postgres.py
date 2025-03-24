import pandas as pd
import json
import sys
import os
from sqlalchemy import MetaData, Table, insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_dir)

from src.utils.create_engine_postgres import create_engine_postgres

def update_ibge00_agregados_municipios_2022(json_file_path, layer):
    if layer == "bronze":
        engine = create_engine_postgres(see_echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        metadata = MetaData()
        IbgeAgregadosMunicipios2022 = Table('ibge00_agregados_municipios_2022', metadata, autoload_with=engine)

        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                raw_json = json.load(file)

            insert_stmt = insert(IbgeAgregadosMunicipios2022).values(raw_json=raw_json)
            session.execute(insert_stmt)
            session.commit()
            print("Dados inseridos com sucesso na camada bronze!")

        except Exception as e:
            print(f"Erro ao inserir dados na camada bronze: {e}")
            session.rollback()

        finally:
            session.close()

if __name__ == "__main__":
    json_path = r'data\outputs\ibge00_agregados_municipios_2022\bronze\2025-03-23_21-52-33\ibge00_agregados_municipios_2022.json'
    layer = "bronze"
    update_ibge00_agregados_municipios_2022(json_path, layer)