import re

from dao.cliente_dao import ClienteDAO
from model.cliente import Cliente


class ClienteController:
    def __init__(self):
        self.cliente_dao = ClienteDAO()

    def _validar_telefone(self, telefone: str):
        telefone_limpo = re.sub(r"\D", "", telefone)
        if len(telefone_limpo) < 10 or len(telefone_limpo) > 11:
            return False, "Telefone inválido. Informe DDD + número (10 ou 11 dígitos)."
        return True, telefone_limpo

    def salvar_cliente(self, nome: str, telefone: str):
        if not nome.strip() or not telefone.strip():
            return False, "Nome e telefone são obrigatórios."

        valido, resultado = self._validar_telefone(telefone)
        if not valido:
            return False, resultado

        cliente = Cliente(None, nome.strip(), telefone.strip())
        return self.cliente_dao.salvar(cliente)

    def atualizar_cliente(self, id_cliente: int, nome: str, telefone: str):
        if not nome.strip() or not telefone.strip():
            return False, "Nome e telefone são obrigatórios."

        valido, resultado = self._validar_telefone(telefone)
        if not valido:
            return False, resultado

        cliente = Cliente(id_cliente, nome.strip(), telefone.strip())
        return self.cliente_dao.atualizar(cliente)

    def listar_clientes(self, filtro_nome: str = ""):
        try:
            return self.cliente_dao.listar(filtro_nome)
        except Exception as e:
            print(f"Erro ao listar clientes: {e}")
            return []

    def buscar_por_id(self, id_cliente: int):
        return self.cliente_dao.buscar_por_id(id_cliente)

    def remover_cliente(self, id_cliente: int):
        if not id_cliente:
            return False, "Cliente não informado."
        return self.cliente_dao.remover(id_cliente)
