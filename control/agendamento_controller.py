import re
from datetime import datetime

from dao.agendamento_dao import AgendamentoDAO
from dao.pet_dao import PetDAO
from model.agendamento import Agendamento


class AgendamentoController:
    def __init__(self):
        self.agendamento_dao = AgendamentoDAO()
        self.pet_dao = PetDAO()

    def _validar_data(self, data: str):
        data = data.strip()
        for formato in ("%d/%m/%Y", "%Y-%m-%d"):
            try:
                datetime.strptime(data, formato)
                if formato == "%d/%m/%Y":
                    dia, mes, ano = data.split("/")
                    return True, f"{ano}-{mes}-{dia}"
                return True, data
            except ValueError:
                continue
        return False, "Data inválida. Use o formato DD/MM/AAAA."

    def _validar_hora(self, hora: str):
        hora = hora.strip()
        if not re.fullmatch(r"\d{2}:\d{2}", hora):
            return False, "Hora inválida. Use o formato HH:MM."
        hora_obj = datetime.strptime(hora, "%H:%M")
        if hora_obj.hour < 8 or hora_obj.hour > 18:
            return False, "Horário deve estar entre 08:00 e 18:00."
        return True, hora

    def salvar_agendamento(self, data: str, hora: str, pet_id: int):
        if not data.strip() or not hora.strip():
            return False, "Data e hora são obrigatórias."
        if not pet_id:
            return False, "Selecione um pet."

        if not self.pet_dao.buscar_por_id(pet_id):
            return False, "Pet não encontrado."

        valido_data, data_formatada = self._validar_data(data)
        if not valido_data:
            return False, data_formatada

        valido_hora, hora_formatada = self._validar_hora(hora)
        if not valido_hora:
            return False, hora_formatada

        if self.agendamento_dao.existe_conflito(pet_id, data_formatada, hora_formatada):
            return False, "Já existe agendamento para este pet no mesmo horário."

        agendamento = Agendamento(None, data_formatada, hora_formatada, pet_id)
        return self.agendamento_dao.salvar(agendamento)

    def atualizar_agendamento(self, id_agendamento: int, data: str, hora: str, pet_id: int):
        if not data.strip() or not hora.strip():
            return False, "Data e hora são obrigatórias."
        if not pet_id:
            return False, "Selecione um pet."

        valido_data, data_formatada = self._validar_data(data)
        if not valido_data:
            return False, data_formatada

        valido_hora, hora_formatada = self._validar_hora(hora)
        if not valido_hora:
            return False, hora_formatada

        if self.agendamento_dao.existe_conflito(
            pet_id, data_formatada, hora_formatada, id_agendamento
        ):
            return False, "Já existe agendamento para este pet no mesmo horário."

        agendamento = Agendamento(id_agendamento, data_formatada, hora_formatada, pet_id)
        return self.agendamento_dao.atualizar(agendamento)

    def listar_agendamentos(self):
        try:
            return self.agendamento_dao.listar_todos()
        except Exception as e:
            print(f"Erro ao listar agendamentos: {e}")
            return []

    def buscar_por_id(self, id_agendamento: int):
        return self.agendamento_dao.buscar_por_id(id_agendamento)

    def remover_agendamento(self, id_agendamento: int):
        if not id_agendamento:
            return False, "Agendamento não informado."
        return self.agendamento_dao.remover(id_agendamento)

    def formatar_data_exibicao(self, data: str):
        try:
            return datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            return data
