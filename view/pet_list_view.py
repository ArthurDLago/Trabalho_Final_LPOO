import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import tkinter as tk
from tkinter import messagebox, ttk

from control.pet_controller import PetController


class JanelaListagemPets(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Pets Cadastrados")
        self.geometry("820x420")

        self.controller = PetController()
        self.criar_widgets()
        self.carregar_dados()

    def criar_widgets(self):
        tk.Label(self, text="Pets Cadastrados", font=("Helvetica", 16, "bold")).pack(pady=10)

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

        colunas = ("ID", "Nome", "Espécie", "Cliente")
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
        tk.Button(frame_botoes, text="Ver Informações", width=15, command=self.mostrar_info).pack(
            side="left", padx=5
        )
        tk.Button(frame_botoes, text="Remover", width=10, command=self.remover_pet).pack(side="left", padx=5)
        tk.Button(frame_botoes, text="Fechar", width=10, command=self.destroy).pack(side="right", padx=5)

    def limpar_filtro(self):
        self.txt_filtro.delete(0, tk.END)
        self.carregar_dados()

    def _obter_id_selecionado(self):
        selecionado = self.tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um pet.", parent=self)
            return None
        return int(self.tree.item(selecionado[0])["values"][0])

    def abrir_novo(self):
        from view.pet_view import JanelaCadastroPet

        janela = JanelaCadastroPet(self)
        self.wait_window(janela)
        self.carregar_dados()

    def abrir_editar(self):
        id_pet = self._obter_id_selecionado()
        if id_pet is None:
            return

        pet = self.controller.buscar_por_id(id_pet)
        if not pet:
            messagebox.showerror("Erro", "Pet não encontrado.", parent=self)
            return

        from view.pet_view import JanelaCadastroPet

        janela = JanelaCadastroPet(self, pet_existente=pet)
        self.wait_window(janela)
        self.carregar_dados()

    def mostrar_info(self):
        id_pet = self._obter_id_selecionado()
        if id_pet is None:
            return

        pet = self.controller.buscar_por_id(id_pet)
        if pet:
            messagebox.showinfo("Informações do Pet", pet.exibir_dados(), parent=self)
        else:
            messagebox.showerror("Erro", "Pet não encontrado.", parent=self)

    def remover_pet(self):
        id_pet = self._obter_id_selecionado()
        if id_pet is None:
            return

        if messagebox.askyesno("Confirmar", f"Remover o pet ID {id_pet}?", parent=self):
            sucesso, msg = self.controller.remover_pet(id_pet)
            if sucesso:
                messagebox.showinfo("Sucesso", msg, parent=self)
                self.carregar_dados()
            else:
                messagebox.showerror("Erro", msg, parent=self)

    def carregar_dados(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        pets = self.controller.listar_pets(self.txt_filtro.get())
        for pet in pets:
            nome_cliente = getattr(pet, "_nome_cliente", "-")
            self.tree.insert(
                "",
                "end",
                values=(pet.get_id(), pet.get_nome(), pet.get_especie(), nome_cliente),
            )
