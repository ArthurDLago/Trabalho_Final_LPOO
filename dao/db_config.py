import psycopg2
from psycopg2 import Error

from conexao import conectar


class DatabaseConfig:
    @staticmethod
    def get_connection():
        try:
            return conectar()
        except Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None
