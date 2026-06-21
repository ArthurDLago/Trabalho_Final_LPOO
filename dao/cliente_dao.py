import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.cliente import Cliente
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class ClienteDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, cliente: Cliente):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "INSERT INTO cliente (nome, telefone) VALUES (%s, %s) RETURNING id",
                (cliente.get_nome(), cliente.get_telefone()),
            )
            cliente._id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Cliente cadastrado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao cadastrar cliente: {e}"
        finally:
            if cursor:
                cursor.close()

    def inserir(self, cliente: Cliente):
        return self.salvar(cliente)

    def listar_todos(self):
        return self.listar()

    def listar(self, filtro_nome: str = ""):
        if not self.conexao:
            return []

        cursor = None
        try:
            cursor = self.conexao.cursor()
            if filtro_nome:
                cursor.execute(
                    "SELECT id, nome, telefone FROM cliente WHERE LOWER(nome) LIKE LOWER(%s) ORDER BY nome",
                    (f"%{filtro_nome.strip()}%",),
                )
            else:
                cursor.execute("SELECT id, nome, telefone FROM cliente ORDER BY nome")

            return [Cliente(row[0], row[1], row[2]) for row in cursor.fetchall()]
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_cliente: int):
        if not self.conexao:
            return None

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT id, nome, telefone FROM cliente WHERE id = %s",
                (id_cliente,),
            )
            row = cursor.fetchone()
            if row:
                return Cliente(row[0], row[1], row[2])
            return None
        except Exception as e:
            print(f"Erro ao buscar cliente: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, cliente: Cliente):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "UPDATE cliente SET nome = %s, telefone = %s WHERE id = %s",
                (cliente.get_nome(), cliente.get_telefone(), cliente.get_id()),
            )
            self.conexao.commit()
            return True, "Cliente atualizado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar cliente: {e}"
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_cliente: int):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM cliente WHERE id = %s", (id_cliente,))
            self.conexao.commit()
            return True, "Cliente removido com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover cliente: {e}"
        finally:
            if cursor:
                cursor.close()

    def deletar(self, id_cliente: int):
        return self.remover(id_cliente)
