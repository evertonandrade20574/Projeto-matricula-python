# =====================================================
# IMPORTAÇÃO DE BIBLIOTECAS
# =====================================================

# Biblioteca principal utilizada para construção
# da interface gráfica desktop.
import tkinter as tk

# Componente responsável pela exibição de mensagens,
# alertas e caixas de confirmação ao usuário.
from tkinter import messagebox

# Bibliotecas da Pillow utilizadas para carregamento,
# redimensionamento e exibição de imagens na interface.
from PIL import Image, ImageTk

# Cliente oficial utilizado para conexão e manipulação
# de dados armazenados no MongoDB Atlas.
from pymongo import MongoClient

# Biblioteca utilizada para manipulação de caminhos
# e localização de arquivos do sistema.
import os


# =====================================================
# CONFIGURAÇÕES GERAIS DA APLICAÇÃO
# =====================================================

# Cor principal utilizada como fundo da aplicação.
BG = "#0D2344"

# Cor padrão utilizada para textos.
FG = "white"


# =====================================================
# CONEXÃO COM O MONGODB
# =====================================================

# Estabelece conexão com o banco de dados hospedado
# no MongoDB Atlas.
client = MongoClient("mongodb+srv://vertonandrade2005_db_user:phanthon@phanthon.pgzyhpu.mongodb.net/?appName=phanthon")

# Seleciona o banco responsável pelo armazenamento
# dos dados acadêmicos da aplicação.
db = client["phantom_matriculas"]

# Coleção utilizada para armazenamento dos alunos.
colecao_alunos = db["alunos"]

# Coleção utilizada para armazenamento das solicitações
# realizadas pelos alunos.
colecao_solicitacoes = db["solicitacoes"]

# Cria um índice único para impedir a existência de
# alunos com o mesmo RGM.
colecao_alunos.create_index("rgm", unique=True)


# =====================================================
# COMPONENTES BASE DA INTERFACE
# =====================================================

# Responsável pela criação do cabeçalho padrão
# exibido em todas as telas da aplicação.
def header():

    # Cria a área superior da interface.
    frame = tk.Frame(root, bg="#081C34", height=50)

    # Faz o cabeçalho ocupar toda a largura disponível.
    frame.pack(fill="x")

    # Exibe o título principal do sistema.
    tk.Label(
        frame,
        text="Phantom Matrículas",
        bg="#081C34",
        fg="white",
        font=("Arial", 14, "bold")
    ).pack(pady=10)


# Responsável por remover todos os componentes
# atualmente renderizados na janela.
def limpar_tela():

    # Percorre todos os widgets ativos.
    for widget in root.winfo_children():

        # Remove o componente da interface.
        widget.destroy()

    # Reconstrói o cabeçalho padrão.
    header()


# Cria um container centralizado utilizado
# como base para todas as telas do sistema.
def criar_container():

    # Cria frame principal.
    frame = tk.Frame(root, bg=BG)

    # Centraliza o frame dentro da janela.
    frame.place(relx=0.5, rely=0.55, anchor="center")

    return frame


# Cria labels padronizadas para manter
# consistência visual em toda aplicação.
def criar_label(parent, texto, size=10, bold=False):

    return tk.Label(
        parent,
        text=texto,
        bg=BG,
        fg=FG,
        font=("Arial", size, "bold" if bold else "normal")
    )


# Cria botões reutilizáveis com identidade visual
# padronizada e efeito hover.
def criar_botao(parent, texto, comando):

    btn = tk.Button(
        parent,
        text=texto,
        command=comando,
        bg="#2563EB",
        fg="white",
        width=22,
        height=2,
        relief="flat",
        cursor="hand2",
        font=("Arial", 10, "bold")
    )

    # Efeito visual executado quando o cursor
    # entra na área do botão.
    def on_enter(e):

        btn.config(bg="#1D4ED8")

    # Restaura a cor padrão quando o cursor
    # deixa a área do botão.
    def on_leave(e):

        btn.config(bg="#2563EB")

    # Registro dos eventos de interação.
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

    return btn


# Cria campos de entrada contendo placeholders
# simulando comportamento semelhante ao HTML.
def criar_entry_placeholder(parent, texto):

    entry = tk.Entry(
        parent,
        fg="grey",
        width=28,
        font=("Arial", 10),
        relief="solid",
        bd=1
    )

    # Define texto inicial orientando o usuário.
    entry.insert(0, texto)

    # Remove o placeholder ao receber foco.
    def on_focus_in(event):

        if entry.get() == texto:

            entry.delete(0, tk.END)

            entry.config(fg="black")

    # Restaura o placeholder quando o campo
    # permanece vazio após perder foco.
    def on_focus_out(event):

        if entry.get() == "":

            entry.insert(0, texto)

            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)

    entry.bind("<FocusOut>", on_focus_out)

    return entry


# Retorna somente o valor informado pelo usuário,
# desconsiderando o texto placeholder.
def valor_real(entry, placeholder):

    return "" if entry.get() == placeholder else entry.get()


# Responsável pelo carregamento e tratamento
# de imagens utilizadas na interface.
def carregar_imagem(nome, w=200, h=200):

    try:

        # Localiza a imagem no diretório do projeto.
        caminho = os.path.join(os.path.dirname(__file__), nome)

        # Abre o arquivo de imagem.
        img = Image.open(caminho)

        # Redimensiona a imagem preservando qualidade.
        img = img.resize((w, h), Image.LANCZOS)

        # Converte a imagem para utilização no Tkinter.
        return ImageTk.PhotoImage(img)

    except:

        # Retorna None caso a imagem não seja encontrada
        # ou ocorra qualquer falha no carregamento.
        return None

    # ==========================================================
# REGRAS DE NEGÓCIO
# ==========================================================
# Esta seção concentra toda a lógica responsável pelo
# gerenciamento dos alunos e das solicitações acadêmicas.
#
# As funções implementadas realizam:
# - Validação de dados
# - Consultas ao MongoDB
# - Atualizações cadastrais
# - Controle de solicitações
# - Regras administrativas
#
# O objetivo é manter a lógica de negócio separada da
# interface gráfica, facilitando manutenção e escalabilidade.
# ==========================================================

# Busca aluno pelo RGM
#
# Funcionalidade:
# Realiza uma consulta no banco de dados utilizando o RGM
# como identificador único do aluno.
#
# Utilizada por diversas funcionalidades do sistema:
# - Login
# - Atribuição de turma
# - Remoção de turma
# - Aprovação de solicitações
#
# Retorno:
# Documento do aluno encontrado ou None.
def buscar_aluno(rgm):

    # Retorna aluno encontrado
    return colecao_alunos.find_one({"rgm": rgm})

# Função para cadastrar aluno
#
# Responsável pelo registro de novos alunos no sistema.
#
# Valida:
# - Campos obrigatórios
# - Formato do RGM
# - Existência de cadastro prévio
#
# Em caso de sucesso:
# - Cria o documento do aluno
# - Armazena os dados no MongoDB
# - Exibe feedback visual ao usuário
def cadastrar_aluno(nome, rgm, curso, horario):

    # Verifica campos obrigatórios
    if not nome or not curso:

        messagebox.showerror(
            "Erro",
            "Preencha todos os campos"
        )

        return

    # Validação do padrão institucional do RGM
    if len(rgm) != 8 or not rgm.isdigit():

        messagebox.showerror(
            "Erro",
            "RGM precisa ter 8 dígitos"
        )

        return

    # Verificação de duplicidade
    if buscar_aluno(rgm):

        messagebox.showerror(
            "Erro",
            "RGM já cadastrado"
        )

        return

    try:

        # Criação do registro acadêmico do aluno
        colecao_alunos.insert_one({
            "nome": nome,
            "rgm": rgm,
            "curso": curso,
            "horario": horario,
            "bolsista": False,
            "turma": None,
            "trocas_nome": 0
        })

        # Feedback de operação concluída
        messagebox.showinfo(
            "Sucesso",
            "Aluno cadastrado"
        )

    except:

        # Tratamento genérico para falhas de persistência
        messagebox.showerror(
            "Erro",
            "Erro ao cadastrar aluno"
        )

# Função para atribuir turma
#
# Permite ao coordenador vincular um aluno
# a uma turma específica.
#
# Fluxo:
# 1. Busca o aluno
# 2. Valida existência
# 3. Atualiza a turma no banco
# 4. Informa o resultado ao usuário
def atribuir_turma(rgm, turma):

    # Busca aluno
    aluno = buscar_aluno(rgm)

    # Verifica se existe
    if not aluno:

        messagebox.showerror(
            "Erro",
            "Aluno não encontrado"
        )

        return

    # Atualiza turma no banco
    colecao_alunos.update_one(
        {"rgm": rgm},
        {"$set": {"turma": turma}}
    )

    # Exibe mensagem de sucesso
    messagebox.showinfo(
        "Sucesso",
        f"{aluno['nome']} agora está na turma {turma}"
    )

# Função para remover aluno da turma
#
# Remove a associação entre aluno e turma.
#
# Utiliza atualização parcial do documento
# mantendo todos os demais dados intactos.
def remover_da_turma(rgm):

    # Busca aluno
    aluno = buscar_aluno(rgm)

    # Verifica existência
    if not aluno:

        messagebox.showerror(
            "Erro",
            "Aluno não encontrado"
        )

        return

    # Remove turma do aluno
    colecao_alunos.update_one(
        {"rgm": rgm},
        {"$set": {"turma": None}}
    )

    # Mensagem de sucesso
    messagebox.showinfo(
        "Sucesso",
        "Aluno removido da turma"
    )

# Função para criar solicitações
#
# Implementa um fluxo administrativo baseado
# em solicitações pendentes.
#
# Em vez de alterar dados diretamente,
# determinadas operações geram solicitações
# que aguardam aprovação do coordenador.
#
# Exemplos:
# - Troca de turma
# - Solicitação de bolsa
# - Alteração de nome
def criar_solicitacao(aluno, tipo, valor=None):

    # Insere solicitação no banco
    colecao_solicitacoes.insert_one({
        "rgm": aluno["rgm"],
        "tipo": tipo,
        "valor": valor
    })

    # Mensagem de sucesso
    messagebox.showinfo(
        "Sucesso",
        "Solicitação enviada"
    )

# Função para solicitar troca de nome
#
# Regra de negócio:
# Cada aluno possui limite de uma alteração
# de nome registrada no sistema.
#
# Antes da criação da solicitação são realizadas
# validações de segurança e consistência.
def solicitar_troca_nome(aluno, novo_nome):

    # Verifica limite de trocas
    if aluno["trocas_nome"] >= 1:

        messagebox.showerror(
            "Erro",
            "Limite atingido"
        )

        return

    # Verifica nome válido
    if not novo_nome:

        messagebox.showerror(
            "Erro",
            "Nome inválido"
        )

        return

    # Cria solicitação de troca de nome
    criar_solicitacao(
        aluno,
        "troca_nome",
        novo_nome
    )

# Função para aprovar solicitações
#
# Responsável pela execução efetiva das
# solicitações cadastradas pelos alunos.
#
# Dependendo do tipo da solicitação,
# diferentes atualizações são realizadas
# na base de dados.
#
# Após a aprovação:
# - A alteração é aplicada
# - A solicitação é removida
# - A interface é atualizada
def aprovar(s):

    # Pergunta confirmação
    if not messagebox.askyesno(
        "Confirmação",
        "Deseja aprovar esta solicitação?"
    ):
        return

    # Busca aluno
    aluno = buscar_aluno(s["rgm"])

    # Verifica existência
    if not aluno:
        return

    # Aprovação troca de turma
    if s["tipo"] == "troca_turma":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {"$set": {"turma": s["valor"]}}
        )

    # Aprovação remoção de turma
    elif s["tipo"] == "remover_turma":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {"$set": {"turma": None}}
        )

    # Aprovação bolsa
    elif s["tipo"] == "bolsa":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {"$set": {"bolsista": True}}
        )

    # Aprovação troca de nome
    elif s["tipo"] == "troca_nome":

        colecao_alunos.update_one(
            {"rgm": aluno["rgm"]},
            {
                "$set": {"nome": s["valor"]},
                "$inc": {"trocas_nome": 1}
            }
        )

    # Remove solicitação aprovada
    colecao_solicitacoes.delete_one(
        {"_id": s["_id"]}
    )

    # Mensagem de sucesso
    messagebox.showinfo(
        "Aprovado",
        "Solicitação aprovada"
    )

    # Atualiza tela
    ver_solicitacoes()

# Função para recusar solicitações
#
# Permite ao coordenador encerrar uma
# solicitação sem aplicar alterações.
#
# A recusa remove apenas o registro da
# solicitação, preservando os dados atuais
# do aluno.
def recusar(s):

    # Pergunta confirmação
    if not messagebox.askyesno(
        "Confirmação",
        "Deseja recusar esta solicitação?"
    ):
        return

    # Remove solicitação
    colecao_solicitacoes.delete_one(
        {"_id": s["_id"]}
    )

    # Mensagem de recusa
    messagebox.showinfo(
        "Recusado",
        "Solicitação recusada"
    )

    # Atualiza tela
    ver_solicitacoes()

    # ==========================================================
# TELAS DO SISTEMA
# ==========================================================
# Esta seção concentra toda a construção visual da aplicação.
#
# O sistema foi desenvolvido utilizando Tkinter para criação
# da interface gráfica desktop.
#
# Cada tela foi encapsulada em funções independentes,
# permitindo:
#
# - Organização do código
# - Facilidade de manutenção
# - Navegação estruturada
# - Reutilização de componentes
#
# A troca entre telas ocorre por meio da função
# limpar_tela(), que remove os componentes atuais e
# recria apenas os elementos necessários para cada fluxo.
# ==========================================================

# Tela inicial do sistema
#
# Ponto de entrada principal da aplicação.
#
# Disponibiliza acesso às duas áreas do sistema:
# - Área do Aluno
# - Área do Coordenador
#
# Também realiza o carregamento da identidade visual
# através do logotipo institucional.
def tela_inicial():

    # Limpa a tela
    limpar_tela()

    # Cria container principal
    frame = criar_container()

    # Carrega imagem
    img = carregar_imagem("phantom.png")

    # Verifica se imagem foi carregada
    if img:

        # Cria label com imagem
        lbl = tk.Label(frame, image=img, bg=BG)

        # Mantém referência da imagem
        lbl.image = img

        # Posiciona imagem
        lbl.grid(row=0, column=0, pady=10)

    # Botão área do aluno
    criar_botao(
        frame,
        "Área do Aluno",
        tela_login_aluno
    ).grid(row=1, column=0, pady=10)

    # Botão área coordenador
    criar_botao(
        frame,
        "Área do Coordenador",
        tela_coordenador
    ).grid(row=2, column=0, pady=10)

# Tela de login do aluno
#
# Responsável pela autenticação simplificada do aluno
# utilizando o RGM como identificador acadêmico.
#
# Após validação dos dados, o usuário é direcionado
# para sua área individual.
def tela_login_aluno():

    limpar_tela()

    frame = criar_container()

    criar_label(
        frame,
        "Login do Aluno",
        14,
        True
    ).grid(row=0, column=0, pady=10)

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "Digite seu RGM"
    )

    rgm.grid(row=1, column=0, pady=5)

    # Botão entrar
    criar_botao(
        frame,
        "Entrar",
        lambda: login_aluno(
            valor_real(rgm, "Digite seu RGM")
        )
    ).grid(row=2, column=0, pady=10)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_inicial
    ).grid(row=3, column=0)

# Função login aluno
#
# Realiza a busca do aluno no banco de dados.
#
# Caso o registro exista:
# - Abre a área do aluno
#
# Caso contrário:
# - Exibe mensagem de erro
def login_aluno(rgm):

    # Busca aluno
    aluno = buscar_aluno(rgm)

    # Se encontrar abre tela aluno
    if aluno:
        tela_aluno(aluno)

    else:

        # Caso contrário mostra erro
        messagebox.showerror(
            "Erro",
            "Aluno não encontrado"
        )

# Tela do aluno
#
# Área destinada às funcionalidades disponíveis
# para o estudante.
#
# Recursos implementados:
# - Solicitação de troca de turma
# - Solicitação de remoção de turma
# - Solicitação de bolsa
# - Solicitação de alteração de nome
#
# Todas as ações são encaminhadas para aprovação
# administrativa.
def tela_aluno(aluno):

    limpar_tela()

    frame = criar_container()

    # Exibe nome e turma
    criar_label(
        frame,
        f"{aluno['nome']} | Turma: {aluno['turma']}",
        12,
        True
    ).grid(row=0, column=0, pady=10)

    # Variável da turma
    turma = tk.StringVar(value="A")

    # Menu de opções de turma
    tk.OptionMenu(
        frame,
        turma,
        "A",
        "B",
        "C"
    ).grid(row=1, column=0)

    # Solicitação troca de turma
    criar_botao(
        frame,
        "Trocar turma",
        lambda: criar_solicitacao(
            aluno,
            "troca_turma",
            turma.get()
        )
    ).grid(row=2, column=0, pady=5)

    # Solicitação remover turma
    criar_botao(
        frame,
        "Remover turma",
        lambda: criar_solicitacao(
            aluno,
            "remover_turma"
        )
    ).grid(row=3, column=0, pady=5)

    # Solicitação bolsa
    criar_botao(
        frame,
        "Solicitar bolsa",
        lambda: criar_solicitacao(
            aluno,
            "bolsa"
        )
    ).grid(row=4, column=0, pady=5)

    # Campo novo nome
    nome = criar_entry_placeholder(
        frame,
        "Novo nome"
    )

    nome.grid(row=5, column=0)

    # Botão troca nome
    criar_botao(
        frame,
        "Trocar nome",
        lambda: solicitar_troca_nome(
            aluno,
            valor_real(nome, "Novo nome")
        )
    ).grid(row=6, column=0, pady=5)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_inicial
    ).grid(row=7, column=0, pady=10)

# Tela coordenador
#
# Painel administrativo principal.
#
# Centraliza todas as operações de gestão
# acadêmica disponíveis ao coordenador.
#
# Funcionalidades:
# - Cadastro de alunos
# - Consulta de registros
# - Gerenciamento de turmas
# - Análise de solicitações
def tela_coordenador():

    limpar_tela()

    frame = criar_container()

    criar_label(
        frame,
        "Painel do Coordenador",
        16,
        True
    ).grid(row=0, column=0, pady=10)

    # Botão cadastrar
    criar_botao(
        frame,
        "Cadastrar",
        tela_cadastro
    ).grid(row=1, column=0, pady=5)

    # Botão listar alunos
    criar_botao(
        frame,
        "Listar",
        listar_alunos
    ).grid(row=2, column=0, pady=5)

    # Botão atribuir turma
    criar_botao(
        frame,
        "Atribuir turma",
        tela_atribuir
    ).grid(row=3, column=0, pady=5)

    # Botão remover turma
    criar_botao(
        frame,
        "Remover turma",
        tela_remover
    ).grid(row=4, column=0, pady=5)

    # Botão solicitações
    criar_botao(
        frame,
        "Solicitações",
        ver_solicitacoes
    ).grid(row=5, column=0, pady=5)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_inicial
    ).grid(row=6, column=0, pady=10)

# Tela cadastro de aluno
#
# Formulário responsável pelo registro
# de novos alunos no sistema acadêmico.
#
# Os dados coletados são enviados para a
# camada de regras de negócio, onde são
# realizadas todas as validações necessárias.
def tela_cadastro():

    limpar_tela()

    frame = criar_container()

    # Campo nome
    nome = criar_entry_placeholder(
        frame,
        "Nome"
    )

    nome.grid(row=0, column=0)

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "RGM (8 Digitos)"
    )

    rgm.grid(row=1, column=0)

    # Campo curso
    curso = criar_entry_placeholder(
        frame,
        "Curso"
    )

    curso.grid(row=2, column=0)

    # Variável horário
    horario = tk.StringVar(value="Manhã")

    # Menu horário
    tk.OptionMenu(
        frame,
        horario,
        "Manhã",
        "Tarde",
        "Noite"
    ).grid(row=3, column=0)

    # Botão cadastrar
    criar_botao(
        frame,
        "Cadastrar",
        lambda: cadastrar_aluno(
            valor_real(nome, "Nome"),
            valor_real(rgm, "RGM"),
            valor_real(curso, "Curso"),
            horario.get()
        )
    ).grid(row=4, column=0)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=5, column=0)

# Tela atribuir turma
#
# Interface administrativa destinada à
# vinculação de alunos às turmas disponíveis.
#
# Permite selecionar uma turma e atualizar
# o cadastro do aluno diretamente no banco.
def tela_atribuir():

    limpar_tela()

    frame = criar_container()

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "RGM do aluno"
    )

    rgm.grid(row=0, column=0)

    # Variável turma
    turma = tk.StringVar(value="A")

    # Menu turmas
    tk.OptionMenu(
        frame,
        turma,
        "A",
        "B",
        "C"
    ).grid(row=1, column=0)

    # Botão atribuir
    criar_botao(
        frame,
        "Atribuir",
        lambda: atribuir_turma(
            valor_real(rgm, "RGM do aluno"),
            turma.get()
        )
    ).grid(row=2, column=0)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=3, column=0)

    # Tela remover turma
#
# Interface administrativa destinada à remoção
# de vínculos entre alunos e turmas.
#
# O coordenador informa o RGM do aluno e o sistema
# executa a atualização diretamente na base de dados.
#
# Essa funcionalidade é útil para remanejamentos,
# correções cadastrais e reorganização acadêmica.
def tela_remover():

    limpar_tela()

    frame = criar_container()

    # Campo RGM
    rgm = criar_entry_placeholder(
        frame,
        "RGM do aluno"
    )

    rgm.grid(row=0, column=0)

    # Botão remover
    criar_botao(
        frame,
        "Remover",
        lambda: remover_da_turma(
            valor_real(rgm, "RGM do aluno")
        )
    ).grid(row=1, column=0)

    # Botão voltar
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=2, column=0)

# Tela listar alunos
#
# Responsável pela visualização dos registros
# armazenados no banco de dados.
#
# A listagem é apresentada em formato tabular,
# permitindo rápida consulta das principais
# informações acadêmicas:
#
# - Nome
# - RGM
# - Curso
# - Turma
# - Situação de bolsa
#
# Os dados exibidos são obtidos diretamente
# da coleção de alunos do MongoDB.
def listar_alunos():

    limpar_tela()

    frame = criar_container()

    # Cria tabela
    tabela = tk.Frame(frame, bg="#112D4E")

    tabela.grid(row=0, column=0)

    # Estrutura de cabeçalho da tabela
    headers = [
        "Nome",
        "RGM",
        "Curso",
        "Turma",
        "Status"
    ]

    # Geração dinâmica dos cabeçalhos
    for col, h in enumerate(headers):

        tk.Label(
            tabela,
            text=h,
            bg="#1E3A5F",
            fg="white",
            font=("Arial", 10, "bold"),
            width=12,
            relief="solid",
            bd=1
        ).grid(row=0, column=col)

    # Consulta de todos os alunos cadastrados
    alunos = colecao_alunos.find()

    # Construção dinâmica das linhas da tabela
    for i, aluno in enumerate(alunos, start=1):

        dados = [
            aluno["nome"],
            aluno["rgm"],
            aluno["curso"],
            aluno["turma"] if aluno["turma"] else "-",
            "Bolsista" if aluno["bolsista"] else "Normal"
        ]

        # Renderização das células da tabela
        for j, valor in enumerate(dados):

            tk.Label(
                tabela,
                text=valor,
                bg="#112D4E",
                fg="white",
                font=("Arial", 9),
                width=12,
                relief="solid",
                bd=1
            ).grid(row=i, column=j)

    # Botão de retorno ao painel administrativo
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=1, column=0, pady=10)

# Tela de solicitações
#
# Centraliza o fluxo de aprovação administrativa.
#
# Todas as solicitações enviadas pelos alunos
# são apresentadas nesta interface para análise.
#
# Funcionalidades avaliadas:
# - Troca de turma
# - Remoção de turma
# - Solicitação de bolsa
# - Alteração de nome
#
# O coordenador pode aprovar ou recusar cada
# solicitação individualmente.
def ver_solicitacoes():

    limpar_tela()

    frame = criar_container()

    # Recupera todas as solicitações pendentes
    solicitacoes = colecao_solicitacoes.find()

    # Percorre cada solicitação encontrada
    for i, s in enumerate(solicitacoes):

        # Busca aluno relacionado à solicitação
        aluno = buscar_aluno(s["rgm"])

        if not aluno:
            continue

        # Criação visual do card de solicitação
        card = tk.Frame(
            frame,
            bg="#112D4E",
            bd=1,
            relief="solid",
            padx=10,
            pady=8
        )

        card.grid(
            row=i,
            column=0,
            pady=6,
            sticky="ew"
        )

        # Montagem da descrição da solicitação
        texto = f"{aluno['nome']} → {s['tipo']}"

        if s["valor"]:
            texto += f" ({s['valor']})"

        # Exibição da descrição
        tk.Label(
            card,
            text=texto,
            bg="#112D4E",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(
            side="left",
            expand=True,
            fill="x"
        )

        # Área destinada aos botões de ação
        botoes = tk.Frame(
            card,
            bg="#112D4E"
        )

        botoes.pack(side="right")

        # Botão de aprovação
        #
        # Executa a regra de negócio responsável
        # pela aplicação definitiva da solicitação.
        tk.Button(
            botoes,
            text="✔",
            command=lambda sol=s: aprovar(sol),
            bg="#16A34A",
            fg="white",
            width=3
        ).pack(side="left", padx=2)

        # Botão de recusa
        #
        # Remove a solicitação sem alterar os
        # dados acadêmicos do aluno.
        tk.Button(
            botoes,
            text="✖",
            command=lambda sol=s: recusar(sol),
            bg="#DC2626",
            fg="white",
            width=3
        ).pack(side="left", padx=2)

    # Botão de retorno ao painel do coordenador
    criar_botao(
        frame,
        "Voltar",
        tela_coordenador
    ).grid(row=100, column=0, pady=10)

# ==========================================================
# INICIALIZAÇÃO DA APLICAÇÃO
# ==========================================================
#
# Esta seção realiza a configuração principal
# do sistema desktop.
#
# Responsabilidades:
#
# - Criação da janela principal
# - Definição do título da aplicação
# - Configuração visual
# - Carregamento da tela inicial
# - Inicialização do loop de eventos
#
# O método mainloop() mantém a interface
# ativa aguardando interações do usuário.
# ==========================================================

# Cria janela principal
root = tk.Tk()

# Define título exibido na barra da aplicação
root.title("Phantom Matrículas - Sistema Acadêmico")

# Define dimensões iniciais da janela
root.geometry("400x500")

# Aplica identidade visual principal
root.configure(bg=BG)

# Carrega a primeira tela do sistema
tela_inicial()

# Inicia o loop principal de eventos do Tkinter
#
# A aplicação permanecerá em execução até que
# o usuário encerre a janela.
root.mainloop()