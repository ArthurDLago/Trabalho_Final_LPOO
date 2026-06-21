import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk


class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pet Shop - LPOO")
        self.geometry("520x320")

        lbl = tk.Label(
            self,
            text="Sistema de Gestão de Pet Shop",
            font=("Helvetica", 18, "bold"),
        )
        lbl.pack(pady=40)

        lbl_info = tk.Label(
            self,
            text="Utilize o menu superior para acessar as funcionalidades.",
            font=("Helvetica", 11),
        )
        lbl_info.pack(pady=10)

        self._criar_menu()

    def _criar_menu(self):
        menubar = tk.Menu(self)

        menu_cadastro = tk.Menu(menubar, tearoff=0)
        menu_cadastro.add_command(label="Clientes", command=self._abrir_clientes)
        menu_cadastro.add_command(label="Pets", command=self._abrir_pets)
        menu_cadastro.add_command(label="Agendamentos", command=self._abrir_agendamentos)
        menubar.add_cascade(label="Cadastro", menu=menu_cadastro)

        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self._abrir_sobre)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.config(menu=menubar)

    def _abrir_clientes(self):
        from view.cliente_list_view import JanelaListagemClientes

        JanelaListagemClientes(self)

    def _abrir_pets(self):
        from view.pet_list_view import JanelaListagemPets

        JanelaListagemPets(self)

    def _abrir_agendamentos(self):
        from view.agendamento_list_view import JanelaListagemAgendamentos

        JanelaListagemAgendamentos(self)

    def _abrir_sobre(self):
        from view.sobre_view import JanelaSobre

        JanelaSobre(self)
