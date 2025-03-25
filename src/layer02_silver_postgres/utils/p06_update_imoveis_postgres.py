import pandas as pd
import sys
import os
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.append(root_dir)

from src.utils.create_engine_postgres import create_engine_postgres

def update_zapimoveis(csv_path, layer):
    if layer == "silver":
        engine = create_engine_postgres(see_echo=True)

        Session = sessionmaker(bind=engine)
        session= Session()

        metadata = MetaData(schema='silver')
        Imovel = Table('zapimoveis', metadata, autoload_with=engine)
     
        df = pd.read_csv(csv_path, encoding='utf-8')

        try:
            with Session() as session:
                for index, row in df.iterrows():
                    registro = session.query(Imovel).filter_by(
                        property_id=row['property_id']
                    ).first()
                    if registro:
                        session.execute(
                            Imovel.update()
                            .where(Imovel.c.property_id == row['property_id'])
                            .values(
                                state_city = row['state_city'],
                                location = row['location'],
                                street = row['street'],
                                type_realese = row['type_realese'],
                                area = row['area'],
                                rooms = row['rooms'],
                                bathrooms = row['bathrooms'],
                                price = row['price'],
                                link = row['link'],
                                update_at = row['update_at']
                            )
                        )
                    else:
                        session.execute(
                            Imovel.insert().values(
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
                        )
                session.commit()

        except SQLAlchemyError as e:
            print(f"Erro ao inserir ou atualizar dados: {e}")
            session.rollback()
            
        finally:
            session.close()

if __name__ == "__main__":
    csv_path = r'data\outputs\ZapImoveis\silver\2025-03-22_14-01-01\ZapImoveis-2025-03-22_14-01-01.csv'    
    layer = "silver"
    update_zapimoveis(csv_path, layer)