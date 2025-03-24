import pandas as pd
import sys
import os
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_dir)

from src.utils.create_engine_postgres import create_engine_postgres

def update_ibge00_agregados_municipios_2022(csv_path, layer):
    if layer == "silver":
        engine = create_engine_postgres(see_echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        metadata = MetaData(schema='silver')
        IbgeAgregadosMunicipios2022 = Table('ibge00_agregados_municipios_2022', metadata, autoload_with=engine)

        df = pd.read_csv(csv_path, encoding='utf-8')

        try:
            with Session() as session:
                for index, row in df.iterrows():
                    registro = session.query(IbgeAgregadosMunicipios2022).filter_by(
                        agregado_id=row['Agregado_ID']
                    ).first()
                    if registro:
                        session.execute(
                            IbgeAgregadosMunicipios2022.update()
                            .where(IbgeAgregadosMunicipios2022.c.agregado_id == row['Agregado_ID'])
                            .values(
                                categoria_id=row['Categoria_ID'],
                                categoria_nome=row['Categoria_Nome'],
                                agregado_nome=row['Agregado_Nome']
                            )
                        )
                    else:
                        session.execute(
                            IbgeAgregadosMunicipios2022.insert().values(
                                categoria_id=row['Categoria_ID'],
                                categoria_nome=row['Categoria_Nome'],
                                agregado_id=row['Agregado_ID'],
                                agregado_nome=row['Agregado_Nome']
                            )
                        )
                session.commit()

        except SQLAlchemyError as e:
            print(f"Erro ao inserir ou atualizar dados: {e}")
            session.rollback()

        finally:
            session.close()

if __name__ == "__main__":
    csv_path = r'data\outputs\ibge00_agregados_municipios_2022\silver\2025-03-23_15-59-01\ibge00_agregados_municipios_2022-2025-03-23_15-59-01.csv'
    layer = "silver"
    update_ibge00_agregados_municipios_2022(csv_path, layer)