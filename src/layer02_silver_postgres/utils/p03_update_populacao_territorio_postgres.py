import pandas as pd
import sys
import os
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from unidecode import unidecode

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_dir)

from src.utils.create_engine_postgres import create_engine_postgres

def update_ibge03_populacao_territorio(csv_path, layer):
    if layer == "silver":

        engine = create_engine_postgres(see_echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        metadata = MetaData(schema='silver')
        IbgePopulacaoTerritorio = Table('ibge03_populacao_territorio', metadata, autoload_with=engine)

        df = pd.read_csv(csv_path, encoding='utf-8')

        try:
            with Session() as session:
                for index, row in df.iterrows():
                    registro = session.query(IbgePopulacaoTerritorio).filter_by(
                        id_localidade=row['id_localidade'],
                        serie=row['serie'],
                        id_pesquisa=row['id_pesquisa']
                    ).first()
                    if registro:
                        session.execute(
                            IbgePopulacaoTerritorio.update()
                            .where(IbgePopulacaoTerritorio.c.id_localidade == row['id_localidade'])
                            .where(IbgePopulacaoTerritorio.c.id_nivel == row['id_nivel'])
                            .where(IbgePopulacaoTerritorio.c.id_pesquisa == row['id_pesquisa'])
                            .values(
                                nome_pesquisa=unidecode(str(row['nome_pesquisa'])),
                                unidade=unidecode(str(row['unidade'])),
                                id_nivel=row['id_nivel'],
                                nome_nivel=unidecode(str(row['nome_nivel'])),
                                nome_localidade=unidecode(str(row['nome_localidade'])),
                                valor_serie=row['valor_serie']
                            )
                        )
                    else:
                        session.execute(
                            IbgePopulacaoTerritorio.insert().values(
                                id_pesquisa=row['id_pesquisa'],
                                nome_pesquisa=unidecode(str(row['nome_pesquisa'])),
                                unidade=unidecode(str(row['unidade'])),
                                id_localidade=row['id_localidade'],
                                id_nivel=row['id_nivel'],
                                nome_nivel=unidecode(str(row['nome_nivel'])),
                                nome_localidade=unidecode(str(row['nome_localidade'])),
                                serie=row['serie'],
                                valor_serie=row['valor_serie']
                            )
                        )
                session.commit()


        except SQLAlchemyError as e:
            print(f"Erro ao inserir ou atualizar dados: {e}")
            session.rollback()

        finally:
            session.close()

if __name__ == "__main__":
    csv_path = r'data\outputs\ibge03_populacao_territorio\silver\2025-03-23_19-37-23\ibge03_populacao_territorio-2025-03-23_19-37-23.csv'
    layer = "silver"
    update_ibge03_populacao_territorio(csv_path, layer)