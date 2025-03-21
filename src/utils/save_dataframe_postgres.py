import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# Carregar variáveis de ambiente
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")  # Corrigido o nome da variável
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

def create_connection():
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT
        )

        print("Conexão com o banco de dados criada com sucesso.")
        return conn
    except Exception as e:
        print(f"Erro na conexão com o banco de dados: {e}")
        return None


def create_table(conn, create_query):
    try:
        cursor = conn.cursor()
        cursor.execute(create_query)
        conn.commit()
        cursor.close()
        print("Tabela criada com sucesso.")
    except Exception as e:
        print(f"Erro ao tentar criar tabela: {e}")
        return None


def save_to_database(df, table_name):
    try:
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print("Dados adicionados/atualizados na tabela com sucesso")
    except Exception as e:
        print(f"Erro ao tentar adicionar/atualizar dados na tabela: {e}")
        return None