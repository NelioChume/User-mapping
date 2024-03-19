import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Variáveis de ambiente para conexão ao banco de dados PostgreSQL
DB_DATABASE = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect():
    try:
        # Conectando ao banco de dados
        conn = psycopg2.connect(dbname=DB_DATABASE, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        print("Conexão bem-sucedida!")
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)

def create_database_and_table():
    # Conectar-se ao PostgreSQL
    conn = connect()
    if conn:
        try:
            # Criar um cursor
            cur = conn.cursor()

            # Criar a base de dados "mapping_user" se ainda não existir
            cur.execute("CREATE DATABASE IF NOT EXISTS mapping_user;")
            
            # Conectar-se à base de dados "mapping_user"
            conn.close()
            conn = psycopg2.connect(dbname="mapping_user", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
            cur = conn.cursor()

            # Criar a tabela "authentication_logs" se ainda não existir
            cur.execute("""
                CREATE TABLE IF NOT EXISTS authentication_logs (
                    id SERIAL PRIMARY KEY,
                    container_name VARCHAR(255),
                    authentication_event VARCHAR(255),
                    username VARCHAR(255),
                    exception TEXT,
                    datetime TIMESTAMP
                );
            """)

            # Commit das alterações
            conn.commit()

            # Fechar o cursor e a conexão
            cur.close()
            conn.close()
            print("Base de dados e tabela criadas com sucesso!")
        except psycopg2.Error as e:
            print("Erro ao executar comandos SQL:", e)

if __name__ == "__main__":
    create_database_and_table()
