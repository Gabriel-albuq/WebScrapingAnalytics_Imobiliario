import pandas as pd
import sys
import os
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.utils.create_engine_postgres import create_engine_postgres

Base = declarative_base()
class Imovel(Base):
    __tablename__ = 'zapimoveis'
    
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

Session = sessionmaker(bind=engine)
session= Session()

csv_path = r'data\outputs\ZapImoveis\silver\2025-03-22_14-01-01\ZapImoveis-2025-03-22_14-01-01.csv'       
df = pd.read_csv(csv_path, encoding='utf-8')

try:
    with Session() as session:
        for index, row in df.iterrows():
            imovel = session.query(Imovel).filter_by(property_id=row['property_id']).first()
            if imovel:
                imovel.state_city = row['state_city']
                imovel.location = row['location']
                imovel.street = row['street']
                imovel.type_realese = row['type_realese']
                imovel.area = row['area']
                imovel.rooms = row['rooms']
                imovel.bathrooms = row['bathrooms']
                imovel.price = row['price']
                imovel.link = row['link']
                imovel.update_at = row['update_at']
            else:
                imovel = Imovel(
                    property_id=row['property_id'],
                    state_city=row['state_city'],
                    location=row['location'],
                    street=row['street'],
                    type_realese=row['type_realese'],
                    area=row['area'],
                    rooms=row['rooms'],
                    bathrooms=row['bathrooms'],
                    price=row['price'],
                    link=row['link'],
                    update_at=row['update_at']
                )
                session.add(imovel)
        session.commit()

except SQLAlchemyError as e:
    print(f"Erro ao inserir ou atualizar dados: {e}")