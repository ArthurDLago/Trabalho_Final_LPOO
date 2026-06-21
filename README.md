# Projeto Final LPOO - Pet Shop

Sistema de gestão de pet shop desenvolvido em Python com interface gráfica (Tkinter), persistência em PostgreSQL e arquitetura MVC.

## Descrição geral

O sistema permite cadastrar **clientes**, **pets** e **agendamentos** de serviços (banho, tosa, etc.). Cada pet pertence a um cliente, e cada agendamento está vinculado a um pet, conforme os diagramas UML do projeto.

## Estrutura do projeto

```
model/       → classes de domínio (Cliente, Pet, Agendamento)
dao/         → camada de persistência (DAO)
control/     → regras de negócio e validações
view/        → interface gráfica Tkinter
sql/         → scripts de criação das tabelas
diagramas/   → diagramas UML do sistema
```

## Diagrama de classes

![Diagrama de Classes](diagramas/Modelagem.png)

## Padrões de projeto

1. **DAO (Data Access Object)** — camada `dao/` com CRUD completo para Cliente, Pet e Agendamento.
2. **Factory Method** — `PetFactory` em `model/pet.py` cria instâncias de `Cachorro`, `Gato`, `Ave` ou `OutroPet` conforme a espécie informada.

## Como executar

1. Instale a dependência:
   ```bash
   pip install psycopg2-binary
   ```

2. Configure o PostgreSQL e crie o banco `Trabalho_Final_LPOO` (credenciais em `conexao.py`).

3. Execute o script SQL:
   ```bash
   psql -U postgres -d Trabalho_Final_LPOO -f sql/schema.sql
   ```

4. Inicie o sistema:
   ```bash
   python main.py
   ```

## Funcionalidades

- CRUD completo de **Clientes** (com filtro por nome e validação de telefone)
- CRUD completo de **Pets** (associados a clientes, com Factory por espécie)
- CRUD completo de **Agendamentos** (validação de data/hora e conflito de horário)
- Menu de navegação entre telas
- Tela **Sobre** com informações do sistema e autor

## Declaração de uso de IA

- [x] Utilizei IA como ferramenta de apoio.
- **Ferramenta:** Cursor (Composer)
- **Finalidade:** apoio na estruturação do projeto, implementação das camadas DAO/Controller/View e documentação.
- **Validação:** Todo o código gerado foi revisado e adaptado ao padrão do projeto de referência da disciplina.
