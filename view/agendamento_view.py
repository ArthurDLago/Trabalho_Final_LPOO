import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk

from control.agendamento_controller import AgendamentoController
from control.pet_controller import PetController


class JanelaCadastroAgendamento(tk.Toplevel):
    def __init__(self, master=None, agendamento_existente=None):
        super().__init__(master)
        self.agendamento_existente = agendamento_existente
        self.agendamento_controller = AgendamentoController()
        self.pet_controller = PetController()

        self.title("Atualizar Agendamento" if agendamento_existente else "Novo Agendamento")
        self.geometry("460x280")

        titulo = "Atualizar Agendamento" if agendamento_existente else "Novo Agendamento"
        tk.Label(self, text=titulo, font=("Helvetica", 16, "bold")).pack(pady=10)

        frame_data = tk.Frame(self)
        frame_data.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_data, text="Data (DD/MM/AAAA):").pack(side="left")
        self.txt_data = tk.Entry(frame_data)
        self.txt_data.pack(side="right", expand=True, fill="x")

        frame_hora = tk.Frame(self)
        frame_hora.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_hora, text="Hora (HH:MM):").pack(side="left")
        self.txt_hora = tk.Entry(frame_hora)
        self.txt_hora.pack(side="right", expand=True, fill="x")

        frame_pet = tk.Frame(self)
        frame_pet.pack(pady=5, fill="x", padx=20)
        tk.Label(frame_pet, text="Pet:").pack(side="left")
        self.cb_pet = ttk.Combobox(frame_pet, state="readonly")
        self.cb_pet.pack(side="right", expand=True, fill="x")

        self._carregar_pets()

        texto_botao = "Atualizar" if agendamento_existente else "Salvar"
        tk.Button(self, text=texto_botao, command=self.salvar).pack(pady=20)

        if agendamento_existente:
            self.txt_data.insert(
                0,
                self.agendamento_controller.formatar_data_exibicao(
                    agendamento_existente.get_data()
                ),
            )
            self.txt_hora.insert(0, agendamento_existente.get_hora())
            self._selecionar_pet(agendamento_existente.get_pet_id())

    def _carregar_pets(self):
        pets = self.pet_controller.listar_pets()
        self.mapa_pets = {}
        opcoes = []
        for pet in pets:
            nome_cliente = getattr(pet, "_nome_cliente", "-")
            texto = f"{pet.get_id()} - {pet.get_nome()} ({nome_cliente})"
            opcoes.append(texto)
            self.mapa_pets[texto] = pet.get_id()
        self.cb_pet["values"] = opcoes
        if opcoes:
            self.cb_pet.current(0)

    def _selecionar_pet(self, pet_id: int):
        for texto, pid in self.mapa_pets.items():
            if pid == pet_id:
                self.cb_pet.set(texto)
                return

    def _obter_pet_id(self):
        selecionado = self.cb_pet.get()
        return self.mapa_pets.get(selecionado)

    def salvar(self):
        data = self.txt_data.get()
        hora = self.txt_hora.get()
        pet_id = self._obter_pet_id()

        if self.agendamento_existente:
            sucesso, msg = self.agendamento_controller.atualizar_agendamento(
                self.agendamento_existente.get_id(), data, hora, pet_id
            )
        else:
            sucesso, msg = self.agendamento_controller.salvar_agendamento(data, hora, pet_id)

        if sucesso:
            messagebox.showinfo("Sucesso", msg, parent=self)
            self.destroy()
        else:
            messagebox.showerror("Erro", msg, parent=self)
