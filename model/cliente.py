class Cliente:
    def __init__(self, id: int, nome: str, telefone: str):
        self._id = id
        self._nome = nome
        self._telefone = telefone

    def get_id(self):
        return self._id

    def get_nome(self):
        return self._nome

    def get_telefone(self):
        return self._telefone