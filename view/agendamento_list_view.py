import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk

from control.agendamento_controller import AgendamentoController


class JanelaListagemAgendamentos(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Agendamentos")
        self.geometry("860x420")

        self.controller = AgendamentoController()
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Agendamentos", font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_tree = tk.Frame(self)
        frame_tree.pack(expand=True, fill="both", padx=20, pady=10)

        scrollbar = ttk.Scrollbar(frame_tree)
        scrollbar.pack(side="right", fill="y")

        colunas = ("ID", "Data", "Hora", "Pet", "Cliente")
        self.tree = ttk.Treeview(
            frame_tree, columns=colunas, show="headings", yscrollcommand=scrollbar.set
        )
        for col in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)

        self.tree.pack(expand=True, fill="both")
        scrollbar.config(command=self.tree.yview)

        frame_botoes = tk.Frame(self)
        frame_botoes.pack(fill="x", padx=20, pady=5)

        tk.Button(frame_botoes, text="Novo", width=10, command=self.abrir_novo).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Editar", width=10, command=self.abrir_editar).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Cancelar", width=10, command=self.cancelar_agendamento).pack(
            side="left", padx=5
        )
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def _obter_id_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um agendamento.", parent=self)
            return None
        return int(self.tree.item(selecionado[0])["values"][0])

    def abrir_novo(self):
        from view.agendamento_view import JanelaCadastroAgendamento

        janela = JanelaCadastroAgendamento(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        id_agendamento = self._obter_id_selecionado()
        if id_agendamento is None:
            return

        agendamento = self.controller.buscar_por_id(id_agendamento)
        if not agendamento:
            messagebox.showerror("Erro", "Agendamento não encontrado.", parent=self)
            return

        from view.agendamento_view import JanelaCadastroAgendamento

        janela = JanelaCadastroAgendamento(self, agendamento_existente=agendamento)
        self.wait_window(janela)
        self.carregar_dados()

    def cancelar_agendamento(self):
        id_agendamento = self._obter_id_selecionado()
        if id_agendamento is None:
            return

        if messagebox.askyesno(
            "Confirmar", f"Cancelar o agendamento ID {id_agendamento}?", parent=self
        ):
            sucesso, msg = self.controller.remover_agendamento(id_agendamento)
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", msg, parent=self)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        agendamentos = self.controller.listar_agendamentos()
        for ag in agendamentos:
            self.tree.insert(
                "",
                "end",
                values=(
                    ag.get_id(),
                    self.controller.formatar_data_exibicao(ag.get_data()),
                    ag.get_hora(),
                    getattr(ag, "_nome_pet", "-"),
                    getattr(ag, "_nome_cliente", "-"),
                ),
            )
