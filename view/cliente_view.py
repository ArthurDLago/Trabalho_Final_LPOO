import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox

from control.cliente_controller import ClienteController


class JanelaCadastroCliente(tk.Toplevel):
    def __init__(self, master=None, cliente_existente=None):
        super().__init__(master)
        self.cliente_existente = cliente_existente
        self.controller = ClienteController()

        self.title("Atualizar Cliente" if cliente_existente else "Cadastro de Cliente")
        self.geometry("420x220")

        titulo = "Atualizar Cliente" if cliente_existente else "Cadastrar Cliente"
        tk.Label(self, text=titulo, font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_nome = tk.Frame(self)
        frame_nome.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_nome, text="Nome:").pack(side="left")
        self.txt_nome = tk.Entry(frame_nome)
        self.txt_nome.pack(side="right", expand=True, fill="x")

        frame_telefone = tk.Frame(self)
        frame_telefone.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_telefone, text="Telefone:").pack(side="left")
        self.txt_telefone = tk.Entry(frame_telefone)
        self.txt_telefone.pack(side="right", expand=True, fill="x")

        texto_botao = "Atualizar" if cliente_existente else "Salvar"
        tk.Button(self, text=texto_botao, command=self.salvar).pack(pady=20)

        if cliente_existente:
            self.txt_nome.insert(0, cliente_existente.get_nome())
            self.txt_telefone.insert(0, cliente_existente.get_telefone())

    def salvar(self):
        nome = self.txt_nome.get()
        telefone = self.txt_telefone.get()

        if self.cliente_existente:
            sucesso, msg = self.controller.atualizar_cliente(
                self.cliente_existente.get_id(), nome, telefone
            )
        else:
            sucesso, msg = self.controller.salvar_cliente(nome, telefone)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
