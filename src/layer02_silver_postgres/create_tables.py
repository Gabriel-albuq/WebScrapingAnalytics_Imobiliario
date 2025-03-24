import pandas as pd
import sys
import os
from sqlalchemy import Column, Integer, String, Text, Float, BigInteger, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()

class IbgeAgregadosMunicipios2022(Base):
    __tablename__ = 'ibge00_agregados_municipios_2022'
    __table_args__ = {'schema': 'silver'}

    categoria_id = Column(String(10))
    categoria_nome = Column(Text)  
    agregado_id = Column(Integer, primary_key=True) 
    agregado_nome = Column(Text)

class IbgeMunicipios(Base):
    __tablename__ = 'ibge01_municipios'
    __table_args__ = {'schema': 'silver'}

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    microrregiao_id = Column(String(50))
    microrregiao_nome = Column(String(50))
    mesorregiao_id = Column(Integer)
    mesorregiao_nome = Column(String(50))
    uf_id = Column(Integer)
    uf_sigla = Column(String(2))
    uf_nome = Column(String(50))
    regiao_id = Column(Integer)
    regiao_sigla = Column(String(2))
    regiao_nome = Column(String(50))

class IbgePib(Base):
    __tablename__ = 'ibge02_pib'
    __table_args__ = {'schema': 'silver'}
    
    id_pesquisa = Column(Integer, primary_key=True)
    nome_pesquisa = Column(String(100), nullable=False)
    unidade = Column(String(50))
    id_nivel = Column(String(50))
    nome_nivel = Column(String(50))
    id_localidade = Column(Integer, ForeignKey('silver.ibge01_municipios.id'), primary_key=True)
    nome_localidade = Column(String(100))
    serie = Column(Integer, primary_key=True)
    valor_serie = Column(Float)

    municipio = relationship('IbgeMunicipios')

class IbgePopulacaoTerritorio(Base):
    __tablename__ = 'ibge03_populacao_territorio'
    __table_args__ = {'schema': 'silver'}
    
    id_pesquisa = Column(Integer, primary_key=True)
    nome_pesquisa = Column(String(100), nullable=False)
    unidade = Column(String(50))
    id_nivel = Column(String(50))
    nome_nivel = Column(String(50))
    id_localidade = Column(Integer, ForeignKey('silver.ibge01_municipios.id'), primary_key=True)
    nome_localidade = Column(String(100))
    serie = Column(Integer, primary_key=True)
    valor_serie = Column(Float)

    municipio = relationship('IbgeMunicipios')

class IbgeEmpregos(Base):
    __tablename__ = 'ibge04_empregos'
    __table_args__ = {'schema': 'silver'}
    
    id_pesquisa = Column(Integer, primary_key=True)
    nome_pesquisa = Column(String(100), nullable=False)
    unidade = Column(String(50))
    id_nivel = Column(String(50))
    nome_nivel = Column(String(50))
    id_localidade = Column(Integer, ForeignKey('silver.ibge01_municipios.id'), primary_key=True)
    nome_localidade = Column(String(100))
    serie = Column(Integer, primary_key=True)
    valor_serie = Column(Float)

    municipio = relationship('IbgeMunicipios')

class IbgeEnsinoSuperior(Base):
    __tablename__ = 'ibge05_ensino_superior'
    __table_args__ = {'schema': 'silver'}
    
    id_pesquisa = Column(Integer, primary_key=True)
    nome_pesquisa = Column(String(100), nullable=False)
    unidade = Column(String(50))
    id_nivel = Column(String(50))
    nome_nivel = Column(String(50))
    id_localidade = Column(Integer, ForeignKey('silver.ibge01_municipios.id'), primary_key=True)
    nome_localidade = Column(String(100))
    serie = Column(Integer, primary_key=True)
    valor_serie = Column(Float)

    municipio = relationship('IbgeMunicipios')

class Imovel(Base):
    __tablename__ = 'zapimoveis'
    __table_args__ = {'schema': 'silver'}
    
    property_id = Column(BigInteger, primary_key=True)
    state_city = Column(String(100), nullable=False)
    location = Column(String(200))
    street = Column(String(200))
    type_realese = Column(String(50))
    area = Column(String(50))
    rooms = Column(String(50))
    bathrooms = Column(String(50))
    price = Column(String(50))
    link = Column(String(200))
    update_at = Column(String(50), primary_key=True)

engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)
