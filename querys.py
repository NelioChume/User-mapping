import conexao_db as conexao
import psycopg2

def create_database_and_table():
    conn = conexao.connect()
    if conn:
        try:
            # Criar um cursor
            cursor = conn.cursor()

            # Código SQL para criar a base de dados "mapping_user" e a tabela "authentication_logs"
            sql_commands = [
                """
                CREATE DATABASE IF NOT EXISTS mapping_user;
                """,
                """
                \c mapping_user;
                """,
                """
                CREATE TABLE IF NOT EXISTS authentication_logs (
                    id SERIAL PRIMARY KEY,
                    container_name VARCHAR(255),
                    authentication_event VARCHAR(255),
                    username VARCHAR(255),
                    exception TEXT,
                    datetime TIMESTAMP
                );
                """
            ]

            # Executar os comandos SQL
            for command in sql_commands:
                cursor.execute(command)

            # Commit das alterações
            conn.commit()

            # Fechar o cursor e a conexão
            cursor.close()
            conn.close()
        except psycopg2.Error as e:
            print("Erro ao executar comandos SQL:", e)

if __name__ == "__main__":
    create_database_and_table()
