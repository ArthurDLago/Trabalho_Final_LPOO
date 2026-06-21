import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk

from control.cliente_controller import ClienteController


class JanelaListagemClientes(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Clientes Cadastrados")
        self.geometry("700x420")

        self.controller = ClienteController()
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Clientes Cadastrados", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_filtro = tk.Frame(self)
        frame_filtro.pack(fill="x", padx=20, pady=5)
        tk.Label(frame_filtro, text="Buscar por nome:").pack(side="left")
        self.txt_filtro = tk.Entry(frame_filtro)
        self.txt_filtro.pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(frame_filtro, text="Filtrar", command=self.carregar_dados).pack(side="left", padx=5)
        tk.Button(frame_filtro, text="Limpar", command=self.limpar_filtro).pack(side="left")

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Nome", "Telefone")
        self.tree = ttk.Treeview(
            frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set
        )
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar", width=10, command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Remover", width=10, command=self.remover_cliente).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def limpar_filtro(self):
        self.txt_filtro.delete(0, tk.END)
        self.carregar_dados()

    def _obter_id_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cliente.", parent=self)
            return None
        return int(self.tree.item(selecionado[0])["values"][0])

    def abrir_novo(self):
        from view.cliente_view import JanelaCadastroCliente

        janela = JanelaCadastroCliente(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        id_cliente = self._obter_id_selecionado()
        if id_cliente is None:
            return

        cliente = self.controller.buscar_por_id(id_cliente)
        if not cliente:
            messagebox.showerror("Erro", "Cliente não encontrado.", parent=self)
            return

        from view.cliente_view import JanelaCadastroCliente

        janela = JanelaCadastroCliente(self, cliente_existente=cliente)
        self.wait_window(janela)
        self.carregar_dados()

    def remover_cliente(self):
        id_cliente = self._obter_id_selecionado()
        if id_cliente is None:
            return

        if messagebox.askyesno("Confirmar", f"Remover o cliente ID {id_cliente}?", parent=self):
            sucesso, msg = self.controller.remover_cliente(id_cliente)
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", msg, parent=self)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtro = self.txt_filtro.get()
        clientes = self.controller.listar_clientes(filtro)
        for cliente in clientes:
            self.tree.insert(
                "",
                "end",
                values=(cliente.get_id(), cliente.get_nome(), cliente.get_telefone()),
            )
