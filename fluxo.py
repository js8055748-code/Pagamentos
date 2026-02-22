import sqlite3
import tkinter as tk
from tkinter import messagebox

# ============================================================
# 1. Conexão com o banco de dados
# ============================================================
conexao = sqlite3.connect("pagamentos.db")
cursor = conexao.cursor()
# Criar tabela se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS titulos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    beneficiario TEXT,
    data TEXT,
    valor REAL,
    status TEXT
)
""")
conexao.commit()

# ============================================================
# 2. Função para cadastrar título
# ============================================================
def cadastrar():
    tipo = entrada_tipo.get()
    descricao = entrada_descricao.get()
    beneficiario = entrada_beneficiario.get()
    data = entrada_data.get()
    valor = entrada_valor.get()
    status = entrada_status.get()
    cursor.execute("""
    INSERT INTO titulos (tipo, descricao, beneficiario, data, valor, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (tipo, descricao, beneficiario, data, valor, status))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Título cadastrado com sucesso!")

# ============================================================
# 3. Função para listar títulos
# ============================================================
def listar():
    cursor.execute("SELECT * FROM titulos")
    registros = cursor.fetchall()
    texto_lista.delete("1.0", tk.END)  # limpa antes de mostrar
    for r in registros:
        texto_lista.insert(tk.END, f"{r}\n")

# ============================================================
# 4. Função para atualizar status
# ============================================================
def atualizar():
    id_titulo = entrada_id.get()
    novo_status = entrada_status.get()
    cursor.execute("UPDATE titulos SET status = ? WHERE id = ?", (novo_status, id_titulo))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")

# ============================================================
# 5. Função para excluir título
# ============================================================
def excluir():
    id_titulo = entrada_id.get()
    cursor.execute("DELETE FROM titulos WHERE id = ?", (id_titulo,))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Título excluído com sucesso!")

# ============================================================
# 6. Construção da janela principal
# ============================================================
janela = tk.Tk()
janela.title("Controle de Pagamentos")

# Campos de entrada
tk.Label(janela, text="Tipo (a pagar / a receber):").grid(row=0, column=0)
entrada_tipo = tk.Entry(janela)
entrada_tipo.grid(row=0, column=1)

tk.Label(janela, text="Descrição:").grid(row=1, column=0)
entrada_descricao = tk.Entry(janela)
entrada_descricao.grid(row=1, column=1)

tk.Label(janela, text="Beneficiário:").grid(row=2, column=0)
entrada_beneficiario = tk.Entry(janela)
entrada_beneficiario.grid(row=2, column=1)

tk.Label(janela, text="Data (AAAA-MM-DD):").grid(row=3, column=0)
entrada_data = tk.Entry(janela)
entrada_data.grid(row=3, column=1)

tk.Label(janela, text="Valor:").grid(row=4, column=0)
entrada_valor = tk.Entry(janela)
entrada_valor.grid(row=4, column=1)

tk.Label(janela, text="Status (pendente/pago):").grid(row=5, column=0)
entrada_status = tk.Entry(janela)
entrada_status.grid(row=5, column=1)

tk.Label(janela, text="ID (para atualizar/excluir):").grid(row=6, column=0)
entrada_id = tk.Entry(janela)
entrada_id.grid(row=6, column=1)

# Botões de ação
tk.Button(janela, text="Cadastrar", bg="green", fg="white", command=cadastrar).grid(row=7, column=0)
tk.Button(janela, text="Listar", command=listar).grid(row=7, column=1)
tk.Button(janela, text="Atualizar Status", command=atualizar).grid(row=8, column=0)
tk.Button(janela, text="Excluir", command=excluir).grid(row=8, column=1)

# Área de texto para mostrar lista
texto_lista = tk.Text(janela, height=10, width=50)
texto_lista.grid(row=9, column=0, columnspan=2)

# ============================================================
# 7. Iniciar o programa
# ============================================================
janela.mainloop()

# ============================================================
# 8. Fechar conexão ao sair
# ============================================================
conexao.close()
