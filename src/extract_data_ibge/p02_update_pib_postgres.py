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
class IbgePibMunicipios(Base):
    __tablename__ = 'ibge02_pib_municipios'
    
    id_localidade = Column(Integer, primary_key=True)
    nome_localidade = Column(String(100), nullable=False)
    id_nivel = Column(String(50))
    nome_nivel = Column(String(50))
    ano = Column(Integer, primary_key=True)
    valor = Column(Integer)

engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


csv_path = r'data\outputs\ibge02_pib_municipios\silver\2025-03-22_12-06-04\ibge02_pib_municipios-2025-03-22_12-06-04.csv'
df = pd.read_csv(csv_path, encoding='utf-8')

try:
    with Session() as session:
        for index, row in df.iterrows():
            pib_municipios = session.query(IbgePibMunicipios).filter_by(id_localidade=row['id_localidade'], ano=row['ano']).first()
            if pib_municipios:
                pib_municipios.nome_localidade = row['nome_localidade']
                pib_municipios.id_nivel = row['id_nivel']
                pib_municipios.nome_nivel = row['nome_nivel']
                pib_municipios.valor = row['valor']
            else:
                pib_municipios = IbgePibMunicipios(
                    id_localidade=row['id_localidade'],
                    nome_localidade=row['nome_localidade'],
                    id_nivel=row['id_nivel'],
                    nome_nivel=row['nome_nivel'],
                    ano=row['ano'],
                    valor=row['valor']
                )
                session.add(pib_municipios)
        session.commit()

except SQLAlchemyError as e:
    print(f"Erro ao inserir ou atualizar dados: {e}")
