class Pet:
    def __init__(self, id: int, nome: str, especie: str, cliente_id: int):
        self._id = id
        self._nome = nome
        self._especie = especie
        self._cliente_id = cliente_id

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_especie(self):
        return self._especie

    def get_cliente_id(self):
        return self._cliente_id