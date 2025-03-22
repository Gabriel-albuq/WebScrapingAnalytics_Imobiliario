import pandas as pd
import sys
import os
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()
class IbgeMunicipios(Base):
    __tablename__ = 'ibge01_municipios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    microrregiao_id = Column(String(50))
    microrregiao_nome = Column(String(50))
    mesorregiao_id= Column(Integer)
    mesorregiao_nome = Column(String(50))
    uf_id = Column(Integer)
    uf_sigla = Column(String(2))
    uf_nome = Column(String(50))
    regiao_id = Column(Integer)
    regiao_sigla = Column(String(2))
    regiao_nome = Column(String(50))
    
engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session= Session()

csv_path = r'data\outputs\ibge01_municipios\silver\2025-03-22_12-05-19\ibge01_municipios-2025-03-22_12-05-19.csv'       
df = pd.read_csv(csv_path, encoding='utf-8')

try:
    with Session() as session:
        for index, row in df.iterrows():
            municipio = session.query(IbgeMunicipios).filter_by(id=row['id']).first()
            if municipio:
                municipio.nome = row['nome']
                municipio.microrregiao_id = row['microrregiao_id']
                municipio.microrregiao_nome = row['microrregiao_nome']
                municipio.mesorregiao_id = row['mesorregiao_id']
                municipio.mesorregiao_nome = row['mesorregiao_nome']
                municipio.uf_id = row['uf_id']
                municipio.uf_sigla = row['uf_sigla']
                municipio.uf_nome = row['uf_nome']
                municipio.regiao_id = row['regiao_id']
                municipio.regiao_sigla = row['regiao_sigla']
                municipio.regiao_nome = row['regiao_nome']
            else:
                municipio = IbgeMunicipios(
                    id=row['id'],
                    nome=row['nome'],
                    microrregiao_id=row['microrregiao_id'],
                    microrregiao_nome=row['microrregiao_nome'],
                    mesorregiao_id=row['mesorregiao_id'],
                    mesorregiao_nome=row['mesorregiao_nome'],
                    uf_id=row['uf_id'],
                    uf_sigla=row['uf_sigla'],
                    uf_nome=row['uf_nome'],
                    regiao_id=row['regiao_id'],
                    regiao_sigla=row['regiao_sigla'],
                    regiao_nome=row['regiao_nome']
                )
                session.add(municipio)
        session.commit()
        
except SQLAlchemyError as e:
    print(f"Erro ao inserir ou atualizar dados: {e}")