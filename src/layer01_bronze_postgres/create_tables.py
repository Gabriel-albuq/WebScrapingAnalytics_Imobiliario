import sys
import os
from sqlalchemy import Column, Integer, String, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()

class BronzeIbgeAgregadosMunicipios2022(Base):
    __tablename__ = 'ibge_00agregados_municipios_2022'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class BronzeIbgeMunicipios(Base):
    __tablename__ = 'ibge_01_municipios'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class BronzeIbgePib(Base):
    __tablename__ = 'ibge_02_pib'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class BronzeIbgePopulacaoTerritorio(Base):
    __tablename__ = 'ibge_03_populacao_territorio'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class BronzeIbgeEmpregos(Base):
    __tablename__ = 'ibge_04_empregos'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class BronzeIbgeEnsinoSuperior(Base):
    __tablename__ = 'ibge_05_ensino_superior'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

class BronzeZapImoveis(Base):
    __tablename__ = 'zapimoveis'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_file = Column(String, nullable=False, unique=True)
    file_json = Column(JSON, nullable=False)

engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)
