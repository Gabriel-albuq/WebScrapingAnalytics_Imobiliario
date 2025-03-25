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
    
def update_ibge01_municipios(csv_path, layer):
    if layer == "silver":
        engine = create_engine_postgres(see_echo=True)

        Session = sessionmaker(bind=engine)
        session= Session()

        metadata = MetaData(schema='silver')
        IbgeMunicipios = Table('ibge01_municipios', metadata, autoload_with=engine)
  
        df = pd.read_csv(csv_path, encoding='utf-8')

        try:
            with Session() as session:
                for index, row in df.iterrows():
                    registro = session.query(IbgeMunicipios).filter_by(
                        id=row['id']
                    ).first()
                    if registro:
                        session.execute(
                            IbgeMunicipios.update()
                            .where(IbgeMunicipios.c.id == row['id'])
                            .values(
                                nome=unidecode(str(row['nome'])),
                                microrregiao_id=row['microrregiao_id'],
                                microrregiao_nome=unidecode(str(row['microrregiao_nome'])),
                                mesorregiao_id=row['mesorregiao_id'],
                                mesorregiao_nome=unidecode(str(row['mesorregiao_nome'])),
                                uf_id=row['uf_id'],
                                uf_sigla=unidecode(str(row['uf_sigla'])),
                                uf_nome=unidecode(str(row['uf_nome'])),
                                regiao_id=row['regiao_id'],
                                regiao_sigla=unidecode(str(row['regiao_sigla'])),
                                regiao_nome=unidecode(str(row['regiao_nome']))
                            )
                        )
                    else:
                        session.execute(
                            IbgeMunicipios.insert().values(
                                id=row['id'],
                                nome=unidecode(str(row['nome'])),
                                microrregiao_id=row['microrregiao_id'],
                                microrregiao_nome=unidecode(str(row['microrregiao_nome'])),
                                mesorregiao_id=row['mesorregiao_id'],
                                mesorregiao_nome=unidecode(str(row['mesorregiao_nome'])),
                                uf_id=row['uf_id'],
                                uf_sigla=unidecode(str(row['uf_sigla'])),
                                uf_nome=unidecode(str(row['uf_nome'])),
                                regiao_id=row['regiao_id'],
                                regiao_sigla=unidecode(str(row['regiao_sigla'])),
                                regiao_nome=unidecode(str(row['regiao_nome']))
                            )
                        )
                session.commit()
                
        except SQLAlchemyError as e:
            print(f"Erro ao inserir ou atualizar dados: {e}")
            session.rollback()

        finally:
            session.close()

if __name__ == "__main__":
    csv_path = r'data\outputs\ibge01_municipios\silver\2025-03-22_12-05-19\ibge01_municipios-2025-03-22_12-05-19.csv'
    layer = "silver"
    update_ibge01_municipios(csv_path, layer)