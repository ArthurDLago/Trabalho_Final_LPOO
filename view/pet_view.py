import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk

from control.cliente_controller import ClienteController
from control.pet_controller import PetController


class JanelaCadastroPet(tk.Toplevel):
    def __init__(self, master=None, pet_existente=None):
        super().__init__(master)
        self.pet_existente = pet_existente
        self.pet_controller = PetController()
        self.cliente_controller = ClienteController()

        self.title("Atualizar Pet" if pet_existente else "Cadastro de Pet")
        self.geometry("460x300")

        titulo = "Atualizar Pet" if pet_existente else "Cadastrar Pet"
        tk.Label(self, text=titulo, font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_nome = tk.Frame(self)
        frame_nome.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_nome, text="Nome:").pack(side="left")
        self.txt_nome = tk.Entry(frame_nome)
        self.txt_nome.pack(side="right", expand=True, fill="x")

        frame_especie = tk.Frame(self)
        frame_especie.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_especie, text="Espécie:").pack(side="left")
        self.cb_especie = ttk.Combobox(
            frame_especie, values=["cachorro", "gato", "ave", "outro"], state="readonly"
        )
        self.cb_especie.current(0)
        self.cb_especie.pack(side="right", expand=True, fill="x")

        frame_cliente = tk.Frame(self)
        frame_cliente.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_cliente, text="Cliente:").pack(side="left")
        self.cb_cliente = ttk.Combobox(frame_cliente, state="readonly")
        self.cb_cliente.pack(side="right", expand=True, fill="x")

        self._carregar_clientes()

        texto_botao = "Atualizar" if pet_existente else "Salvar"
        tk.Button(self, text=texto_botao, command=self.salvar).pack(pady=20)

        if pet_existente:
            self.txt_nome.insert(0, pet_existente.get_nome())
            especie = pet_existente.get_especie()
            if especie in ["cachorro", "gato", "ave"]:
                self.cb_especie.set(especie)
            else:
                self.cb_especie.set("outro")
            self._selecionar_cliente(pet_existente.get_cliente_id())

    def _carregar_clientes(self):
        clientes = self.cliente_controller.listar_clientes()
        self.mapa_clientes = {}
        opcoes = []
        for cliente in clientes:
            texto = f"{cliente.get_id()} - {cliente.get_nome()}"
            opcoes.append(texto)
            self.mapa_clientes[texto] = cliente.get_id()
        self.cb_cliente["values"] = opcoes
        if opcoes:
            self.cb_cliente.current(0)

    def _selecionar_cliente(self, cliente_id: int):
        for texto, cid in self.mapa_clientes.items():
            if cid == cliente_id:
                self.cb_cliente.set(texto)
                return

    def _obter_cliente_id(self):
        selecionado = self.cb_cliente.get()
        return self.mapa_clientes.get(selecionado)

    def salvar(self):
        nome = self.txt_nome.get()
        especie = self.cb_especie.get()
        cliente_id = self._obter_cliente_id()

        if self.pet_existente:
            sucesso, msg = self.pet_controller.atualizar_pet(
                self.pet_existente.get_id(), nome, especie, cliente_id
            )
        else:
            sucesso, msg = self.pet_controller.salvar_pet(nome, especie, cliente_id)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
