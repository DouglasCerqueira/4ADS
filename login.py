import customtkinter as ctk
from tkinter import *
import sqlite3
from tkinter import messagebox, ttk
from tkcalendar import Calendar, DateEntry


class BancoUsuarios():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_gosdoçura.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado com sucesso")

    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado com sucesso")

    def cria_tabela_usuarios(self):
        self.conecta_db()
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Usuarios(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Usuario TEXT NOT NULL,
                Email TEXT NOT NULL,
                Telefone TEXT NOT NULL,
                CPF TEXT NOT NULL,
                DataNascimento DATE NOT NULL,
                Senha TEXT NOT NULL,
                Confirma_senha TEXT NOT NULL,
                ehAdmin TEXT
            );                       
        """)
        self.conn.commit()
        print("Tabela criada com sucesso")
        self.desconecta_db()

    def cadastrar_usuario(self):
        self.username_cadastro = self.username_cadastro_entry.get()
        self.email_cadastro = self.email_cadastro_entry.get()
        self.telefone_cadastro = self.telefone_cadastro_entry.get()
        self.cpf_cadastro = self.cpf_cadastro_entry.get()
        self.datanasc_cadastro = self.datanasc_cadastro_entry.get()
        self.senha_cadastro = self.senha_cadastro_entry.get()
        self.confirma_senha_cadastro = self.confirma_senha_cadastro_entry.get()

        self.conecta_db()

        self.cursor.execute(""" 
            INSERT INTO Usuarios (Usuario, Email, Telefone, CPF, DataNascimento, Senha, Confirma_senha, ehAdmin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                            (self.username_cadastro, self.email_cadastro, self.telefone_cadastro, self.cpf_cadastro,
                             self.datanasc_cadastro, self.senha_cadastro, self.confirma_senha_cadastro, "Funcionário"))

        try:
            if (
                    self.username_cadastro == "" or self.email_cadastro == "" or self.telefone_cadastro == "" or self.cpf_cadastro == "" or self.datanasc_cadastro == "" or
                    self.senha_cadastro == "" or self.confirma_senha_cadastro == ""):
                messagebox.showerror(title="Cadastro", message="Preencha todos os campos corretamente.")
            elif (len(self.username_cadastro) < 4):
                messagebox.showwarning(title="Cadastro",
                                       message="O nome de usuário deve possuir pelo menos 4 caracteres.")
            elif (len(self.senha_cadastro) < 4):
                messagebox.showwarning(title="Cadastro", message="Sua senha deve possuir pelo menos 4 caracteres.")
            elif (self.senha_cadastro != self.confirma_senha_cadastro):
                messagebox.showerror(title="Cadastro", message="A senha não são identicas.")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Cadastro", message="Cadastro efetuado com sucesso.")
                self.desconecta_db()
                self.limpa_entry_cadastro()
        except:
            messagebox.showerror(title="Cadastro", message="Erro no cadastro. Tente Novamente!")
            self.desconecta_db()

    def verifica_login(self):
        self.username_login = self.username_login_entry.get()
        self.senha_login = self.senha_login_entry.get()
        self.escolha_login = self.seleciona_conta.get()

        self.conecta_db()
        self.cursor.execute("""SELECT * FROM Usuarios WHERE (Usuario = ? AND Senha = ? AND ehAdmin = ?)""",
                            (self.username_login, self.senha_login, self.escolha_login))

        self.verifica_dados = self.cursor.fetchone()

        try:
            if (self.username_login == "" or self.senha_login == ""):
                messagebox.showwarning(title="Login", message="Digite todos os dados.")
            elif (
                    self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados and self.escolha_login == "Administrador" in self.verifica_dados):
                messagebox.showinfo(title="Login", message="Login efetuado.")
                app.destroy()
                PaginaAdministrador()
                self.desconecta_db()
            elif (
                    self.username_login in self.verifica_dados and self.senha_login in self.verifica_dados and self.escolha_login == "Funcionário" in self.verifica_dados):
                messagebox.showinfo(title="Login", message="Login efetuado.")
                app.destroy()
                PaginaFuncionario()
                self.desconecta_db()
        except:
            messagebox.showerror(title="Login", message="Usuário ou senha incorretos!")
            self.desconecta_db()


class BancoClientes():
    def conecta_db(self):
        self.conn = sqlite3.connect("Sistema_gosdoçura.db")
        self.cursor = self.conn.cursor()
        print("Banco de dados conectado com sucesso")

    def desconecta_db(self):
        self.conn.close()
        print("Banco de dados desconectado com sucesso")

    def cria_tabela_clientes(self):
        self.conecta_db()
        self.cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS Clientes(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Email TEXT NOT NULL,
                Telefone TEXT NOT NULL,
                CPF TEXT NOT NULL,
                DataNascimento DATE NOT NULL
            );                       
        """)
        self.conn.commit()
        print("Tabela criada com sucesso")
        self.desconecta_db()

    def cadastrar_clientes(self):
        self.nome_cliente = self.nome_entry.get()
        self.email_cliente = self.email_entry.get()
        self.telefone_cliente = self.telefone_entry.get()
        self.cpf_cliente = self.cpf_entry.get()
        self.datanasc_cliente = self.datanasc_entry.get()

        self.conecta_db()

        self.cursor.execute(""" 
            INSERT INTO Clientes (Nome, Email, Telefone, CPF, DataNascimento)
            VALUES (?, ?, ?, ?, ?)""", (self.nome_cliente, self.email_cliente, self.telefone_cliente, self.cpf_cliente,
                                        self.datanasc_cliente))

        try:
            if (
                    self.nome_cliente == "" or self.email_cliente == "" or self.telefone_cliente == "" or self.cpf_cliente == ""):
                messagebox.showerror(title="Cadastro", message="Preencha todos os campos corretamente.")
            else:
                self.conn.commit()
                messagebox.showinfo(title="Cadastro", message="Cadastro efetuado com sucesso.")
                self.lista_clientes()
                self.desconecta_db()
                self.limpa_cadastro_cliente()
        except:
            messagebox.showerror(title="Cadastro", message="Erro no cadastro. Tente Novamente!")
            self.desconecta_db()

    def lista_clientes(self):
        self.conecta_db()

        self.lista_cliente = []
        self.cursor.execute("""SELECT * FROM Clientes""")

        self.guarda_dados = self.cursor.fetchall()

        for self.i in self.guarda_dados:
            self.lista_cliente.append(self.i)

        self.tabela = ["ID", "NOME", "EMAIL", "TELEFONE", "CPF", "DATA DE NASCIMENTO"]

        self.lista = ttk.Treeview(self.frame_lista, selectmode="extended", columns=self.tabela, show="headings")
        self.vertical = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista.yview)
        self.horizontal = ttk.Scrollbar(self.frame_lista, orient="horizontal", command=self.lista.xview)

        self.lista.configure(yscrollcommand=self.vertical.set, xscrollcommand=self.horizontal.set)
        self.lista.grid(column=0, row=0, sticky='nsew')
        self.vertical.grid(column=1, row=0, sticky='ns')
        self.horizontal.grid(column=0, row=1, sticky='ew')

        self.frame_lista.grid_rowconfigure(0, weight=12)

        self.hd = ["nw", "nw", "nw", "nw", "nw", "nw"]
        self.h = [150, 150, 150, 150, 150, 150]
        self.n = 0

        for col in self.tabela:
            self.lista.heading(col, text=col.title(), anchor=CENTER)
            self.lista.column(col, width=self.h[self.n], anchor=self.hd[self.n])

        self.n += 1

        for item in self.lista_cliente:
            self.lista.insert('', 'end', values=item)

    def atualizar_clientes(self, i):
        self.conecta_db()
        self.cursor.execute("""UPDATE Clientes SET Nome=?, Email=?, Telefone=?, CPF=?, DataNascimento=? WHERE ID=? """,
                            i)

        try:
            self.conn.commit()
            messagebox.showinfo(title="Atualização", message="Atualização realizada com sucesso.")
            self.lista_clientes()
            self.desconecta_db()
            self.limpa_cadastro_cliente()
        except:
            messagebox.showerror(title="Atualização", message="Erro na atualização. Tente Novamente!")
            self.desconecta_db()

    def mostra_cliente(self):
        try:
            self.dados = self.lista.focus()
            self.listar_dados = self.lista.item(self.dados)
            self.listar = self.listar_dados["values"]

            self.id = self.listar[0]

            self.limpa_cadastro_cliente()

            self.nome_entry.insert(0, self.listar[1])
            self.email_entry.insert(0, self.listar[2])
            self.telefone_entry.insert(0, self.listar[3])
            self.cpf_entry.insert(0, self.listar[4])
            self.datanasc_entry.insert(0, self.listar[5])

            def atualizar():
                nome_cliente_update = self.nome_entry.get()
                email_cliente_update = self.email_entry.get()
                telefone_cliente_update = self.telefone_entry.get()
                cpf_cliente_update = self.cpf_entry.get()
                datanasc_cliente_update = self.datanasc_entry.get()

                listagem = [nome_cliente_update, email_cliente_update, telefone_cliente_update, cpf_cliente_update,
                            datanasc_cliente_update, self.id]

                self.atualizar_clientes(listagem)

            self.buttom_confirmar = ctk.CTkButton(self.frame_cadastro, text="Atualizar", width=80,
                                                  font=("Century Gothic", 16), fg_color="green", corner_radius=4,
                                                  command=atualizar)
            self.buttom_confirmar.place(x=120, y=400)
        except IndexError:
            messagebox.showerror(title="Atualização", message="Selecione algum cliente na tabela ao lado.")

    def deletar(self, i):
        self.conecta_db()
        self.cursor.execute("""DELETE FROM Clientes WHERE id=?""", i)

        try:
            self.conn.commit()
            messagebox.showinfo(title="Excluir", message="A exclusão foi realizada com sucesso.")
            self.lista_clientes()
            self.desconecta_db()
        except:
            messagebox.showerror(title="Excluir", message="Erro na exclusão. Tente Novamente!")
            self.desconecta_db()

    def excluir_cliente(self):
        try:
            self.dados = self.lista.focus()
            self.listar_dados = self.lista.item(self.dados)
            self.listar = self.listar_dados["values"]

            self.id = [self.listar[0]]

            self.deletar(self.id)


        except:
            messagebox.showerror(title="Erro", message="Selecione algum cliente na tabela ao lado.")


class App(ctk.CTk, BancoUsuarios):
    def __init__(self):
        super().__init__()
        self.janela_inicial()
        self.tela_login()
        self.cria_tabela_usuarios()

    def janela_inicial(self):
        self.geometry("800x420")
        self.title("Loja Gosdoçura")
        self.resizable(False, False)

    def show_password(self):
        if (self.senha_login_entry.cget("show") == "*" or self.senha_cadastro_entry.cget(
                "show") == "*" or self.confirma_senha_cadastro_entry.cget("show") == "*"):
            self.senha_login_entry.configure(show="")
            self.senha_cadastro_entry.configure(show="")
            self.confirma_senha_cadastro_entry.configure(show="")
        else:
            self.senha_login_entry.configure(show="*")
            self.senha_cadastro_entry.configure(show="*")
            self.confirma_senha_cadastro_entry.configure(show="*")

    def tela_login(self):
        self.img = PhotoImage(file="brigadeiro.png")
        self.img = self.img.subsample(2, 2)
        self.lb_img = ctk.CTkLabel(self, text=None, image=self.img)
        self.lb_img.grid(row=1, column=0, padx=0, pady=25)

        self.title = ctk.CTkLabel(self, text="Faça seu login ou cadastre-se\n na nossa loja Gosdoçura",
                                  font=("Century Gothic", 20), text_color="#964B00")
        self.title.grid(row=0, column=0, padx=30, pady=10)

        self.frame_login = ctk.CTkFrame(self, width=340, height=380)
        self.frame_login.place(x=350, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_login, text="Faça seu Login", font=("Century Gothic", 20))
        self.lb_title.grid(row=1, column=0, padx=10, pady=10)

        self.username_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Nome de Usuário",
                                                 font=("Century Gothic", 16), corner_radius=15)
        self.username_login_entry.grid(row=2, column=0, pady=10, padx=10)

        self.senha_login_entry = ctk.CTkEntry(self.frame_login, width=300, placeholder_text="Senha",
                                              font=("Century Gothic", 16), corner_radius=15, show="*")
        self.senha_login_entry.grid(row=3, column=0, pady=10, padx=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_login, text="Mostrar Senha", font=("Century Gothic", 14),
                                         corner_radius=20, command=self.show_password)
        self.ver_senha.grid(row=4, column=0, pady=10, padx=10)

        opcao_menu = ctk.StringVar(value="Funcionário")
        self.seleciona_conta = ctk.CTkOptionMenu(self.frame_login, values=["Funcionário", "Administrador"],
                                                 variable=opcao_menu, corner_radius=15)
        self.seleciona_conta.grid(row=5, column=0, padx=20, pady=10)

        self.buttom_login = ctk.CTkButton(self.frame_login, width=300, text="Fazer Login", font=("Century Gothic", 16),
                                          corner_radius=15, command=self.verifica_login)
        self.buttom_login.grid(row=6, column=0, pady=10, padx=10)

        self.span = ctk.CTkLabel(self.frame_login, text="Caso seja um funcionário novo? Clique no botão abaixo",
                                 font=("Century Gothic", 15))
        self.span.grid(row=7, column=0, pady=10, padx=10)

        self.buttom_cadastro = ctk.CTkButton(self.frame_login, width=300, text="Cadastre-se",
                                             font=("Century Gothic", 16), corner_radius=15,
                                             fg_color="green", command=self.tela_cadastro)
        self.buttom_cadastro.grid(row=8, column=0, pady=10, padx=10)

    def tela_cadastro(self):
        self.frame_login.place_forget()

        self.frame_cadastro = ctk.CTkFrame(self, width=340, height=380)
        self.frame_cadastro.place(x=450, y=10)

        self.lb_title = ctk.CTkLabel(self.frame_cadastro, text="Faça seu Cadastro", font=("Century Gothic", 20))
        self.lb_title.grid(row=0, column=0, padx=10, pady=3)

        self.username_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Nome de Usuário",
                                                    font=("Century Gothic", 16), corner_radius=15)
        self.username_cadastro_entry.grid(row=1, column=0, pady=3, padx=10)

        self.email_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Email",
                                                 font=("Century Gothic", 16), corner_radius=15)
        self.email_cadastro_entry.grid(row=2, column=0, pady=3, padx=10)

        self.telefone_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Telefone",
                                                    font=("Century Gothic", 16), corner_radius=15)
        self.telefone_cadastro_entry.grid(row=3, column=0, pady=3, padx=10)

        self.cpf_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="CPF",
                                               font=("Century Gothic", 16), corner_radius=15)
        self.cpf_cadastro_entry.grid(row=4, column=0, pady=3, padx=10)

        self.datanasc_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300,
                                                    placeholder_text="Data de Nascimento", font=("Century Gothic", 16),
                                                    corner_radius=15)
        self.datanasc_cadastro_entry.grid(row=5, column=0, pady=3, padx=10)

        self.senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300, placeholder_text="Senha",
                                                 font=("Century Gothic", 16), corner_radius=15, show="*")
        self.senha_cadastro_entry.grid(row=6, column=0, pady=3, padx=10)

        self.confirma_senha_cadastro_entry = ctk.CTkEntry(self.frame_cadastro, width=300,
                                                          placeholder_text="Confirme a Senha",
                                                          font=("Century Gothic", 16),
                                                          corner_radius=15, show="*")
        self.confirma_senha_cadastro_entry.grid(row=7, column=0, pady=3, padx=10)

        self.ver_senha = ctk.CTkCheckBox(self.frame_cadastro, text="Mostrar Senha", font=("Century Gothic", 14),
                                         corner_radius=20, command=self.show_password)
        self.ver_senha.grid(row=8, column=0, pady=3)

        self.buttom_cadastrar = ctk.CTkButton(self.frame_cadastro, width=300, text="Cadastre-se",
                                              font=("Century Gothic", 16), corner_radius=15, fg_color="green",
                                              command=self.cadastrar_usuario)
        self.buttom_cadastrar.grid(row=9, column=0, pady=3, padx=10)

        self.buttom_voltar = ctk.CTkButton(self.frame_cadastro, width=300, text="Voltar", font=("Century Gothic", 16),
                                           corner_radius=15, fg_color="gray",
                                           command=self.tela_login)
        self.buttom_voltar.grid(row=10, column=0, pady=10, padx=10)

    def limpa_entry_cadastro(self):
        self.username_cadastro_entry.delete(0, END)
        self.email_cadastro_entry.delete(0, END)
        self.telefone_cadastro_entry.delete(0, END)
        self.cpf_cadastro_entry.delete(0, END)
        self.datanasc_cadastro_entry.delete(0, END)
        self.senha_cadastro_entry.delete(0, END)
        self.confirma_senha_cadastro_entry.delete(0, END)

    def limpa_entry_login(self):
        self.username_login_entry.delete(0, END)
        self.senha_login_entry.delete(0, END)


class PaginaAdministrador:
    def __init__(self):
        self.janela_administrador = ctk.CTk()
        self.janela_inicial_adm()
        self.escolhas()
        self.janela_administrador.mainloop()

    def janela_inicial_adm(self):
        self.janela_administrador.geometry("220x250")
        self.janela_administrador.title("ADM")
        self.janela_administrador.resizable(False, False)

    def escolhas(self):
        self.crud_clientes = ctk.CTkButton(self.janela_administrador, width=200, text="Aba Clientes",
                                           font=("Century Gothic", 16), corner_radius=15, command=CRUD_Clientes)
        self.crud_clientes.grid(row=0, column=0, pady=10, padx=10)
        self.crud_fornecedores = ctk.CTkButton(self.janela_administrador, width=200, text="Aba Fornecedores",
                                               font=("Century Gothic", 16), corner_radius=15)
        self.crud_fornecedores.grid(row=1, column=0, pady=10, padx=10)
        self.crud_funcionarios = ctk.CTkButton(self.janela_administrador, width=200, text="Aba Funcionarios",
                                               font=("Century Gothic", 16), corner_radius=15)
        self.crud_funcionarios.grid(row=2, column=0, pady=10, padx=10)
        self.crud_produtos = ctk.CTkButton(self.janela_administrador, width=200, text="Aba Produtos",
                                           font=("Century Gothic", 16), corner_radius=15)
        self.crud_produtos.grid(row=3, column=0, pady=10, padx=10)
        self.sair = ctk.CTkButton(self.janela_administrador, width=100, text="Sair", font=("Century Gothic", 16),
                                  corner_radius=15, fg_color="red", hover_color="grey",
                                  command=self.janela_administrador.destroy)
        self.sair.grid(row=4, column=0, pady=10, padx=10)


class PaginaFuncionario:
    def __init__(self):
        self.janela_funcionario = ctk.CTk()
        self.janela_inicial_funcionario()
        self.escolhas()
        self.janela_funcionario.mainloop()

    def janela_inicial_funcionario(self):
        self.janela_funcionario.geometry("220x150")
        self.janela_funcionario.title("FUNCIONÁRIO")
        self.janela_funcionario.resizable(False, False)

    def escolhas(self):
        self.crud_clientes = ctk.CTkButton(self.janela_funcionario, width=200, text="Aba Clientes",
                                           font=("Century Gothic", 16), corner_radius=15, command=CRUD_Clientes)
        self.crud_clientes.grid(row=0, column=0, pady=10, padx=10)
        self.crud_vendas = ctk.CTkButton(self.janela_funcionario, width=200, text="Aba Vendas",
                                         font=("Century Gothic", 16), corner_radius=15)
        self.crud_vendas.grid(row=1, column=0, pady=10, padx=10)
        self.sair = ctk.CTkButton(self.janela_funcionario, width=100, text="Sair", font=("Century Gothic", 16),
                                  corner_radius=15, fg_color="red", hover_color="grey",
                                  command=self.janela_funcionario.destroy)
        self.sair.grid(row=2, column=0, pady=10, padx=10)


class CRUD_Clientes(BancoClientes):
    def __init__(self):
        self.clientes = ctk.CTk()
        self.janela_inicial_crud()
        self.tela_crud()
        self.cria_tabela_clientes()
        self.lista_clientes()
        self.clientes.mainloop()

    def janela_inicial_crud(self):
        self.clientes.geometry("1230x500")
        self.clientes.title("CRUD Clientes")
        self.clientes.resizable(False, False)

    def tela_crud(self):
        self.frame_title = ctk.CTkFrame(self.clientes, width=310, height=50, fg_color="black", corner_radius=0)
        self.frame_title.grid(row=0, column=0)

        self.frame_cadastro = ctk.CTkFrame(self.clientes, width=310, height=500, corner_radius=0)
        self.frame_cadastro.grid(row=1, column=0, sticky=NSEW, padx=0, pady=1)

        self.frame_lista = ctk.CTkFrame(self.clientes, width=588, height=403, corner_radius=0)
        self.frame_lista.grid(row=0, column=1, rowspan=2, padx=1, pady=0, sticky=NSEW)

        self.title = ctk.CTkLabel(self.frame_title, text="Formulário de Cliente", anchor=NW,
                                  font=("Century Gothic", 20), text_color="white", bg_color="black")
        self.title.place(x=50, y=15)

        self.nome = ctk.CTkLabel(self.frame_cadastro, text="Nome", anchor=NW, font=("Century Gothic", 16),
                                 text_color="white")
        self.nome.place(x=10, y=10)
        self.nome_entry = ctk.CTkEntry(self.frame_cadastro, width=280, justify="left", corner_radius=5)
        self.nome_entry.place(x=10, y=35)

        self.email = ctk.CTkLabel(self.frame_cadastro, text="Email", anchor=NW, font=("Century Gothic", 16),
                                  text_color="white")
        self.email.place(x=10, y=75)
        self.email_entry = ctk.CTkEntry(self.frame_cadastro, width=280, justify="left", corner_radius=5)
        self.email_entry.place(x=10, y=100)

        self.telefone = ctk.CTkLabel(self.frame_cadastro, text="Telefone", anchor=NW, font=("Century Gothic", 16),
                                     text_color="white")
        self.telefone.place(x=10, y=140)
        self.telefone_entry = ctk.CTkEntry(self.frame_cadastro, width=280, justify="left", corner_radius=5)
        self.telefone_entry.place(x=10, y=165)

        self.cpf = ctk.CTkLabel(self.frame_cadastro, text="CPF", anchor=NW, font=("Century Gothic", 16),
                                text_color="white")
        self.cpf.place(x=10, y=205)
        self.cpf_entry = ctk.CTkEntry(self.frame_cadastro, width=280, justify="left", corner_radius=5)
        self.cpf_entry.place(x=10, y=230)

        self.datanasc = ctk.CTkLabel(self.frame_cadastro, text="Data de Nascimento", anchor=NW,
                                     font=("Century Gothic", 16), text_color="white")
        self.datanasc.place(x=10, y=270)
        self.datanasc_entry = DateEntry(self.frame_cadastro, width=12, background="darkblue", foreground="white",
                                        borderwidth=2, date_pattern="dd/mm/yyyy")
        self.datanasc_entry.place(x=10, y=295)

        self.buttom_cadastrar = ctk.CTkButton(self.frame_cadastro, text="Cadastrar", width=80,
                                              font=("Century Gothic", 16), fg_color="blue", corner_radius=4,
                                              command=self.cadastrar_clientes)
        self.buttom_cadastrar.place(x=10, y=360)

        self.buttom_atualizar = ctk.CTkButton(self.frame_cadastro, text="Alterar", width=80,
                                              font=("Century Gothic", 16), fg_color="green", corner_radius=4,
                                              command=self.mostra_cliente)
        self.buttom_atualizar.place(x=120, y=360)

        self.buttom_deletar = ctk.CTkButton(self.frame_cadastro, text="Excluir", width=80, font=("Century Gothic", 16),
                                            fg_color="red", corner_radius=4,
                                            command=self.excluir_cliente)
        self.buttom_deletar.place(x=220, y=361)

    def limpa_cadastro_cliente(self):
        self.nome_entry.delete(0, END)
        self.email_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cpf_entry.delete(0, END)
        self.datanasc_entry.delete(0, END)


if __name__ == "__main__":
    app = App()
    app.mainloop()