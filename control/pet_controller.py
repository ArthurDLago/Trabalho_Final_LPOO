from dao.pet_dao import PetDAO
from model.pet import PetFactory


class PetController:
    ESPECIES = ["cachorro", "gato", "ave", "outro"]

    def __init__(self):
        self.pet_dao = PetDAO()

    def salvar_pet(self, nome: str, especie: str, cliente_id: int):
        if not nome.strip():
            return False, "Nome do pet é obrigatório."
        if not cliente_id:
            return False, "Selecione um cliente."
        if not especie.strip():
            return False, "Espécie do pet é obrigatória."

        try:
            pet = PetFactory.criar_pet(especie.strip(), None, nome.strip(), cliente_id)
            return self.pet_dao.salvar(pet)
        except ValueError as e:
            return False, str(e)

    def atualizar_pet(self, id_pet: int, nome: str, especie: str, cliente_id: int):
        if not nome.strip():
            return False, "Nome do pet é obrigatório."
        if not cliente_id:
            return False, "Selecione um cliente."
        if not especie.strip():
            return False, "Espécie do pet é obrigatória."

        try:
            pet = PetFactory.criar_pet(especie.strip(), id_pet, nome.strip(), cliente_id)
            return self.pet_dao.atualizar(pet)
        except ValueError as e:
            return False, str(e)

    def listar_pets(self, filtro_nome: str = ""):
        try:
            return self.pet_dao.listar_todos(filtro_nome)
        except Exception as e:
            print(f"Erro ao listar pets: {e}")
            return []

    def listar_por_cliente(self, cliente_id: int):
        return self.pet_dao.listar_por_cliente(cliente_id)

    def buscar_por_id(self, id_pet: int):
        return self.pet_dao.buscar_por_id(id_pet)

    def remover_pet(self, id_pet: int):
        if not id_pet:
            return False, "Pet não informado."
        return self.pet_dao.remover(id_pet)
