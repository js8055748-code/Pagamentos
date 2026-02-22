import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox


# ============================================================
# 1. Conexão com o banco de dados
# ============================================================
conexao = sqlite3.connect("pagamentos.db")
cursor = conexao.cursor()

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
# 2. Funções principais (cadastro, consulta, atualização, exclusão)
# ============================================================
def cadastrar():
    tipo = entrada_tipo.get().strip()
    descricao = entrada_descricao.get().strip()
    beneficiario = entrada_beneficiario.get().strip()
    data = entrada_data.get().strip()
    valor = entrada_valor.get().strip()
    status = entrada_status.get().strip()

    if tipo not in ["a pagar", "a receber"]:
        messagebox.showerror("Erro", "Tipo deve ser 'a pagar' ou 'a receber'.")
        return
    if descricao == "" or beneficiario == "" or data == "" or valor == "" or status == "":
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return
    try:
        float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Valor deve ser numérico.")
        return
    if status not in ["pendente", "pago"]:
        messagebox.showerror("Erro", "Status deve ser 'pendente' ou 'pago'.")
        return

    cursor.execute("""
    INSERT INTO titulos (tipo, descricao, beneficiario, data, valor, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (tipo, descricao, beneficiario, data, float(valor), status))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Título cadastrado com sucesso!")

def listar():
    cursor.execute("SELECT * FROM titulos")
    registros = cursor.fetchall()
    texto_lista.delete("1.0", tk.END)
    for r in registros:
        texto_lista.insert(tk.END, f"{r}\n")

def atualizar():
    id_titulo = entrada_id.get().strip()
    novo_status = entrada_status_update.get().strip()

    if id_titulo == "" or not id_titulo.isdigit():
        messagebox.showerror("Erro", "Informe um ID válido.")
        return
    if novo_status not in ["pendente", "pago"]:
        messagebox.showerror("Erro", "Status deve ser 'pendente' ou 'pago'.")
        return

    cursor.execute("UPDATE titulos SET status = ? WHERE id = ?", (novo_status, id_titulo))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Status atualizado com sucesso!")

def excluir():
    id_titulo = entrada_id.get().strip()

    if id_titulo == "" or not id_titulo.isdigit():
        messagebox.showerror("Erro", "Informe um ID válido.")
        return

    cursor.execute("DELETE FROM titulos WHERE id = ?", (id_titulo,))
    conexao.commit()
    messagebox.showinfo("Sucesso", "Título excluído com sucesso!")

# ============================================================
# 3. Funções de Relatórios
# ============================================================
def relatorio_pendentes():
    cursor.execute("SELECT * FROM titulos WHERE status = 'pendente'")
    registros = cursor.fetchall()
    texto_relatorio.delete("1.0", tk.END)
    texto_relatorio.insert(tk.END, "--- Títulos Pendentes ---\n")
    for r in registros:
        texto_relatorio.insert(tk.END, f"{r}\n")

def relatorio_totais():
    cursor.execute("SELECT tipo, SUM(valor) FROM titulos GROUP BY tipo")
    registros = cursor.fetchall()
    texto_relatorio.delete("1.0", tk.END)
    texto_relatorio.insert(tk.END, "--- Totais ---\n")
    for r in registros:
        texto_relatorio.insert(tk.END, f"{r[0]}: R$ {r[1]:.2f}\n")

def relatorio_grafico():
    cursor.execute("SELECT tipo, SUM(valor) FROM titulos GROUP BY tipo")
    registros = cursor.fetchall()

    tipos = [r[0] for r in registros]
    valores = [r[1] for r in registros]

    plt.bar(tipos, valores, color=["red", "green"])
    plt.title("Totais a Pagar e a Receber")
    plt.xlabel("Tipo")
    plt.ylabel("Valor Total (R$)")
    plt.show()

# ============================================================
# 4. Construção da janela principal com abas
# ============================================================
janela = tk.Tk()
janela.title("Controle de Pagamentos")

abas = ttk.Notebook(janela)
abas.pack(expand=True, fill="both")

# Aba Cadastro
aba_cadastro = tk.Frame(abas)
abas.add(aba_cadastro, text="Cadastro")

tk.Label(aba_cadastro, text="Tipo (a pagar / a receber):").grid(row=0, column=0)
entrada_tipo = tk.Entry(aba_cadastro)
entrada_tipo.grid(row=0, column=1)

tk.Label(aba_cadastro, text="Descrição:").grid(row=1, column=0)
entrada_descricao = tk.Entry(aba_cadastro)
entrada_descricao.grid(row=1, column=1)

tk.Label(aba_cadastro, text="Beneficiário:").grid(row=2, column=0)
entrada_beneficiario = tk.Entry(aba_cadastro)
entrada_beneficiario.grid(row=2, column=1)

tk.Label(aba_cadastro, text="Data ( dd-mm-aaaa):").grid(row=3, column=0)
entrada_data = tk.Entry(aba_cadastro)
entrada_data.grid(row=3, column=1)

tk.Label(aba_cadastro, text="Valor:").grid(row=4, column=0)
entrada_valor = tk.Entry(aba_cadastro)
entrada_valor.grid(row=4, column=1)

tk.Label(aba_cadastro, text="Status (pendente/pago):").grid(row=5, column=0)
entrada_status = tk.Entry(aba_cadastro)
entrada_status.grid(row=5, column=1)

tk.Button(aba_cadastro, text="Cadastrar", bg="light blue", fg="blue", command=cadastrar).grid(row=7, column=0, columnspan=2)

# Aba Consulta
aba_consulta = tk.Frame(abas)
abas.add(aba_consulta, text="Consulta")

tk.Button(aba_consulta, text="Listar Títulos", command=listar).pack()
texto_lista = tk.Text(aba_consulta, height=15, width=60)
texto_lista.pack()

# Aba Atualização/Exclusão
aba_update = tk.Frame(abas)
abas.add(aba_update, text="Atualizar/Excluir")

tk.Label(aba_update, text="ID do título:").grid(row=0, column=0)
entrada_id = tk.Entry(aba_update)
entrada_id.grid(row=0, column=1)

tk.Label(aba_update, text="Novo Status (pendente/pago):").grid(row=1, column=0)
entrada_status_update = tk.Entry(aba_update)
entrada_status_update.grid(row=1, column=1)

tk.Button(aba_update, text="Atualizar Status", command=atualizar).grid(row=2, column=0)
tk.Button(aba_update, text="Excluir Título", command=excluir).grid(row=2, column=1)

# Aba Relatórios
aba_relatorios = tk.Frame(abas)
abas.add(aba_relatorios, text="Relatórios")

tk.Button(aba_relatorios, text="Mostrar Pendentes", command=relatorio_pendentes).pack()
tk.Button(aba_relatorios, text="Totais a Pagar/Receber", command=relatorio_totais).pack()
tk.Button(aba_relatorios, text="Gráfico Totais", command=relatorio_grafico).pack()
texto_relatorio = tk.Text(aba_relatorios, height=15, width=60)
texto_relatorio.pack()

# ============================================================
# 5. Iniciar programa
# ============================================================
janela.mainloop()
conexao.close()
