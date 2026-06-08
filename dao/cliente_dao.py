from conexao import conectar
from model.cliente import Cliente

class ClienteDAO:

    def inserir(self, cliente: Cliente):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cliente (nome, telefone) VALUES (%s, %s)",
            (cliente.get_nome(), cliente.get_telefone())
        )
        conn.commit()
        cursor.close()
        conn.close()

    def listar(self):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, telefone FROM cliente")
        resultados = cursor.fetchall()

        clientes = []
        for row in resultados:
            clientes.append(Cliente(row[0], row[1], row[2]))

        cursor.close()
        conn.close()
        return clientes

    def atualizar(self, cliente: Cliente):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cliente SET nome=%s, telefone=%s WHERE id=%s",
            (cliente.get_nome(), cliente.get_telefone(), cliente.get_id())
        )
        conn.commit()
        cursor.close()
        conn.close()

    def deletar(self, id: int):
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cliente WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()