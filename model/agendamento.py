class Agendamento:
    def __init__(self, id: int, data: str, hora: str, pet_id: int):
        self._id = id
        self._data = data
        self._hora = hora
        self._pet_id = pet_id

    def get_id(self):
        return self._id

    def get_data(self):
        return self._data

    def get_hora(self):
        return self._hora

    def get_pet_id(self):
        return self._pet_id