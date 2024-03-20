import psycopg2
import os
from dotenv import load_dotenv

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
        # Desabilitar o modo de transação automática
        conn.autocommit = True
        print("Conexão bem-sucedida!")
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao PostgreSQL:", e)

def create_database_if_not_exists(conn, dbname):
    try:
        # Criar um cursor sem iniciar uma transação
        cur = conn.cursor()

        # Verificar se o banco de dados já existe consultando o catálogo do PostgreSQL
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
        exists = cur.fetchone()

        if not exists:
            # Criar o banco de dados se ainda não existir
            cur.execute(f"CREATE DATABASE {dbname};")
            print(f"Banco de dados '{dbname}' criado com sucesso!")
        else:
            print(f"O banco de dados '{dbname}' já existe.")

        # Fechar o cursor
        cur.close()
    except psycopg2.Error as e:
        print("Erro ao executar comandos SQL:", e)

def create_database_and_table():
    # Conectar-se ao PostgreSQL
    conn = connect()
    if conn:
        try:
            # Criar a base de dados "mapping_user" se ainda não existir
            create_database_if_not_exists(conn, "mapping_user")

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

def insert_authentication_log(container_name, authentication_event, username, exception=None, datetime=None):
    try:
        # Conectar-se ao banco de dados
        conn = connect()
        if not conn:
            print("Falha ao conectar ao banco de dados.")
            return
        
        cur = conn.cursor()

        # Inserir os dados na tabela
        cur.execute("""
            INSERT INTO authentication_logs (container_name, authentication_event, username, exception, datetime)
            VALUES (%s, %s, %s, %s, %s);
        """, (container_name, authentication_event, username, exception, datetime))

        # Commit da transação
        conn.commit()

        print("Dados inseridos com sucesso na tabela authentication_logs!")

    except psycopg2.Error as e:
        print("Erro ao inserir dados na tabela authentication_logs:", e)

    finally:
        # Fechar o cursor e a conexão
        if cur:
            cur.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    create_database_and_table()