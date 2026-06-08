from model.cliente import Cliente
from dao.cliente_dao import ClienteDAO

dao = ClienteDAO()

cliente = Cliente(None, "João", "99999-9999")
dao.inserir(cliente)

clientes = dao.listar()
for c in clientes:
    print(c.get_id(), c.get_nome(), c.get_telefone())