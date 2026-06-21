import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.agendamento import Agendamento
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class AgendamentoDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, agendamento: Agendamento):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "INSERT INTO agendamento (data, hora, pet_id) VALUES (%s, %s, %s) RETURNING id",
                (agendamento.get_data(), agendamento.get_hora(), agendamento.get_pet_id()),
            )
            agendamento._id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Agendamento criado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            if "uq_agendamento_pet_data_hora" in str(e):
                return False, "Já existe agendamento para este pet no mesmo horário"
            return False, f"Erro ao criar agendamento: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self):
        if not self.conexao:
            return []

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                """
                SELECT a.id, a.data, a.hora, a.pet_id, p.nome, c.nome
                FROM agendamento a
                INNER JOIN pet p ON p.id = a.pet_id
                INNER JOIN cliente c ON c.id = p.cliente_id
                ORDER BY a.data, a.hora
                """
            )
            agendamentos = []
            for row in cursor.fetchall():
                ag = Agendamento(row[0], str(row[1]), row[2], row[3])
                ag._nome_pet = row[4]
                ag._nome_cliente = row[5]
                agendamentos.append(ag)
            return agendamentos
        except Exception as e:
            print(f"Erro ao listar agendamentos: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_agendamento: int):
        if not self.conexao:
            return None

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                """
                SELECT a.id, a.data, a.hora, a.pet_id, p.nome, c.nome
                FROM agendamento a
                INNER JOIN pet p ON p.id = a.pet_id
                INNER JOIN cliente c ON c.id = p.cliente_id
                WHERE a.id = %s
                """,
                (id_agendamento,),
            )
            row = cursor.fetchone()
            if row:
                ag = Agendamento(row[0], str(row[1]), row[2], row[3])
                ag._nome_pet = row[4]
                ag._nome_cliente = row[5]
                return ag
            return None
        except Exception as e:
            print(f"Erro ao buscar agendamento: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def existe_conflito(self, pet_id: int, data: str, hora: str, id_ignorar: int = None):
        if not self.conexao:
            return False

        cursor = None
        try:
            cursor = self.conexao.cursor()
            if id_ignorar:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM agendamento
                    WHERE pet_id = %s AND data = %s AND hora = %s AND id <> %s
                    """,
                    (pet_id, data, hora, id_ignorar),
                )
            else:
                cursor.execute(
                    """
                    SELECT COUNT(*) FROM agendamento
                    WHERE pet_id = %s AND data = %s AND hora = %s
                    """,
                    (pet_id, data, hora),
                )
            return cursor.fetchone()[0] > 0
        except Exception as e:
            print(f"Erro ao verificar conflito de agendamento: {e}")
            return True
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, agendamento: Agendamento):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "UPDATE agendamento SET data = %s, hora = %s, pet_id = %s WHERE id = %s",
                (
                    agendamento.get_data(),
                    agendamento.get_hora(),
                    agendamento.get_pet_id(),
                    agendamento.get_id(),
                ),
            )
            self.conexao.commit()
            return True, "Agendamento atualizado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            if "uq_agendamento_pet_data_hora" in str(e):
                return False, "Já existe agendamento para este pet no mesmo horário"
            return False, f"Erro ao atualizar agendamento: {e}"
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_agendamento: int):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM agendamento WHERE id = %s", (id_agendamento,))
            self.conexao.commit()
            return True, "Agendamento cancelado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao cancelar agendamento: {e}"
        finally:
            if cursor:
                cursor.close()
