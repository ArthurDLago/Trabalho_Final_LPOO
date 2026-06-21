import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.pet import Pet, PetFactory
from dao.db_config import DatabaseConfig
from dao.generic_dao import GenericDAO


class PetDAO(GenericDAO):
    def __init__(self):
        self.conexao = DatabaseConfig.get_connection()

    def salvar(self, pet: Pet):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "INSERT INTO pet (nome, especie, cliente_id) VALUES (%s, %s, %s) RETURNING id",
                (pet.get_nome(), pet.get_especie(), pet.get_cliente_id()),
            )
            pet._id = cursor.fetchone()[0]
            self.conexao.commit()
            return True, "Pet cadastrado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao cadastrar pet: {e}"
        finally:
            if cursor:
                cursor.close()

    def listar_todos(self, filtro_nome: str = ""):
        if not self.conexao:
            return []

        cursor = None
        try:
            cursor = self.conexao.cursor()
            if filtro_nome:
                cursor.execute(
                    """
                    SELECT p.id, p.nome, p.especie, p.cliente_id, c.nome
                    FROM pet p
                    INNER JOIN cliente c ON c.id = p.cliente_id
                    WHERE LOWER(p.nome) LIKE LOWER(%s)
                    ORDER BY p.nome
                    """,
                    (f"%{filtro_nome.strip()}%",),
                )
            else:
                cursor.execute(
                    """
                    SELECT p.id, p.nome, p.especie, p.cliente_id, c.nome
                    FROM pet p
                    INNER JOIN cliente c ON c.id = p.cliente_id
                    ORDER BY p.nome
                    """
                )

            pets = []
            for row in cursor.fetchall():
                pet = PetFactory.criar_pet(row[2], row[0], row[1], row[3])
                pet._nome_cliente = row[4]
                pets.append(pet)
            return pets
        except Exception as e:
            print(f"Erro ao listar pets: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def listar_por_cliente(self, cliente_id: int):
        if not self.conexao:
            return []

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "SELECT id, nome, especie, cliente_id FROM pet WHERE cliente_id = %s ORDER BY nome",
                (cliente_id,),
            )
            return [
                PetFactory.criar_pet(row[2], row[0], row[1], row[3])
                for row in cursor.fetchall()
            ]
        except Exception as e:
            print(f"Erro ao listar pets do cliente: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def buscar_por_id(self, id_pet: int):
        if not self.conexao:
            return None

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                """
                SELECT p.id, p.nome, p.especie, p.cliente_id, c.nome
                FROM pet p
                INNER JOIN cliente c ON c.id = p.cliente_id
                WHERE p.id = %s
                """,
                (id_pet,),
            )
            row = cursor.fetchone()
            if row:
                pet = PetFactory.criar_pet(row[2], row[0], row[1], row[3])
                pet._nome_cliente = row[4]
                return pet
            return None
        except Exception as e:
            print(f"Erro ao buscar pet: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def atualizar(self, pet: Pet):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute(
                "UPDATE pet SET nome = %s, especie = %s, cliente_id = %s WHERE id = %s",
                (pet.get_nome(), pet.get_especie(), pet.get_cliente_id(), pet.get_id()),
            )
            self.conexao.commit()
            return True, "Pet atualizado com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao atualizar pet: {e}"
        finally:
            if cursor:
                cursor.close()

    def remover(self, id_pet: int):
        if not self.conexao:
            return False, "Sem conexão com o banco de dados"

        cursor = None
        try:
            cursor = self.conexao.cursor()
            cursor.execute("DELETE FROM pet WHERE id = %s", (id_pet,))
            self.conexao.commit()
            return True, "Pet removido com sucesso"
        except Exception as e:
            self.conexao.rollback()
            return False, f"Erro ao remover pet: {e}"
        finally:
            if cursor:
                cursor.close()
