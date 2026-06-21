import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk


class JanelaSobre(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Sobre o Sistema")
        self.geometry("480x320")
        self.resizable(False, False)

        texto = (
            "Sistema de Gestão de Pet Shop\n\n"
            "Desenvolvido para a disciplina de Linguagem de Programação\n"
            "Orientada a Objetos (LPOO) - 2026/1.\n\n"
            "Permite cadastrar clientes, pets e agendamentos de serviços\n"
            "como banho e tosa, com persistência em PostgreSQL.\n\n"
            "Autor: Arthur Lago\n"
            "Padrões de projeto: DAO e Factory Method"
        )

        lbl = tk.Label(self, text=texto, justify="left", font=("Helvetica", 11))
        lbl.pack(padx=20, pady=20)

        tk.Button(self, text="Fechar", width=12, command=self.destroy).pack(pady=10)
