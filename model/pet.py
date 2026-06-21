from abc import ABC, abstractmethod


class Pet(ABC):
    def __init__(self, id: int, nome: str, cliente_id: int):
        self._id = id
        self._nome = nome
        self._cliente_id = cliente_id

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_cliente_id(self):
        return self._cliente_id

    @abstractmethod
    def get_especie(self):
        pass

    @abstractmethod
    def exibir_dados(self):
        pass


class Cachorro(Pet):
    def get_especie(self):
        return "cachorro"

    def exibir_dados(self):
        return (
            f"Pet: {self._nome}\n"
            f"Espécie: Cachorro\n"
            f"Cliente ID: {self._cliente_id}\n"
            f"Cuidados: banho e tosa recomendados a cada 30 dias"
        )


class Gato(Pet):
    def get_especie(self):
        return "gato"

    def exibir_dados(self):
        return (
            f"Pet: {self._nome}\n"
            f"Espécie: Gato\n"
            f"Cliente ID: {self._cliente_id}\n"
            f"Cuidados: escovação e higiene felina"
        )


class Ave(Pet):
    def get_especie(self):
        return "ave"

    def exibir_dados(self):
        return (
            f"Pet: {self._nome}\n"
            f"Espécie: Ave\n"
            f"Cliente ID: {self._cliente_id}\n"
            f"Cuidados: limpeza de gaiola e unhas"
        )


class OutroPet(Pet):
    def __init__(self, id: int, nome: str, cliente_id: int, especie: str):
        super().__init__(id, nome, cliente_id)
        self._especie = especie

    def get_especie(self):
        return self._especie

    def exibir_dados(self):
        return (
            f"Pet: {self._nome}\n"
            f"Espécie: {self._especie.capitalize()}\n"
            f"Cliente ID: {self._cliente_id}\n"
            f"Cuidados: consultar serviços disponíveis no balcão"
        )


class PetFactory:
    @staticmethod
    def criar_pet(especie: str, id: int, nome: str, cliente_id: int):
        tipo = especie.strip().lower()
        if tipo == "cachorro":
            return Cachorro(id, nome, cliente_id)
        if tipo == "gato":
            return Gato(id, nome, cliente_id)
        if tipo == "ave":
            return Ave(id, nome, cliente_id)
        if tipo:
            return OutroPet(id, nome, cliente_id, tipo)
        raise ValueError("Espécie do pet é obrigatória.")
