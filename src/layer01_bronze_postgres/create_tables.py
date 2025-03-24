import pandas as pd
import sys
import os
from sqlalchemy import Column, Integer, String, Text, Float, BigInteger, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()

class IbgeAgregadosMunicipios2022(Base):
    __tablename__ = 'ibge00_agregados_municipios_2022'
    __table_args__ = {'schema': 'bronze'}

    id = Column(Integer, primary_key=True, autoincrement=True)
    raw_json = Column(JSON, nullable=False) 

engine = create_engine_postgres(see_echo=True)
Base.metadata.create_all(engine)
