import streamlit as st
from google.cloud import firestore
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie

# Para rodar o projeto: python -m streamlit run "C:\Users\belle\OneDrive\Documentos\Vs Code\Projeto Final - Gioia Artes\Início.py"
#  Local URL: http://localhost:8501
#  Network URL: http://192.168.1.8:8501
# Ou no terminal: streamlit run Início.py

# Configurações básicas

st.set_page_config(
    page_title="Gioia Artes",
    layout="wide"
)

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = "cliente"

key_dict = dict(st.secrets["firebase"])
db = firestore.Client.from_service_account_info(key_dict)

# Títulos da página

html_code = """
    <h1 style='color: purple;'> Início</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

st.write("Bem-vindo ao site da Gioia Artes!")

# Animação do gato com novelo e texto
st.divider()
col1, col2 = st.columns([1, 2])

with col1:
    def carregar_animacao(url: str):
        requisicao = requests.get(url)
        if requisicao.status_code != 200:
            return None
        return requisicao.json()

    url_animacao = "https://lottie.host/2242bd2b-a6ae-43ca-92ac-6cbe637dd3b5/XqDDv88T0s.json"

    animacaoCat = carregar_animacao(url_animacao)

    st_lottie(animacaoCat, key="animacaoCat", speed=1, loop=True, width=200)

with col2:
    st.space()
    st.text("Aqui o crochê é feito à mão com carinho, delicadeza e identidade.\nCada peça é criada com amor, transformando fios em detalhes únicos para deixar o seu dia a dia mais bonito e especial.\nTrabalhamos com amigurumis, peças variadas de crochê e de tricô.")

# Animação de tricô e texto
st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    st.space()
    st.space()
    st.space()
    st.space()
    st.text("Trabalhamos com peças em crochê que unem beleza, qualidade e personalidade. Tudo é produzido com materiais selecionados, buscando sempre conforto, durabilidade e um toque especial que só o artesanato pode oferecer.\nNa Gioia Artes, você encontra produtos únicos, feitos para quem valoriza o que é autêntico e cheio de significado.")

with col2:
    def carregar_animacao(url: str):
        requisicao = requests.get(url)
        if requisicao.status_code != 200:
            return None
        return requisicao.json()

    url_animacao = "https://lottie.host/0a9a41df-26bf-4bcb-ba1e-5d1d40f831ca/ZVLOPJAHSS.json"

    animacaoCroche = carregar_animacao(url_animacao)

    st_lottie(animacaoCroche, key="animacaoCroche", speed=1, loop=True, width=400)

# Centralização do logo
st.divider()
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    st.caption("Logo da empresa.")
    st.image("img/logo.png", width=200)  #Ajeitar a imagem e por uma legenda bonitinha
    st.caption("A orquídea roxa representa elegância, criatividade e delicadeza, presentes em cada peça feita á mão.")

# Infos

html_code = """
    <h1 style='color: purple;'> Login, Cadastro e Conta</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

st.text("Para receber as novidades e fazer compras, realize o cadastro.\nSe já é um cliente, realize o login.")

# Tirar o press enter

st.markdown("""
<style>
/* Esconde o texto "Press Enter to submit the form" */
[data-testid="InputInstructions"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)



# Menu

optionMenu = option_menu(
    menu_title="Menu", #obrigatorio
    options=["Logar","Cadastrar","Editar Perfil","Recuperar Senha"],#obrigatorio
    icons=["box-arrow-in-right","person","pencil","key"],  #opcional
    menu_icon=["palette"],
    default_index=0, 
)

# Login

if optionMenu == "Logar":
    st.subheader("Login:")

    with st.form("formLogar"):
        usuario = st.text_input("Usuário:", placeholder="Informe o seu usuário..")
        senha = st.text_input("Senha:", placeholder="Informe a sua senha...", type="password")
        btnLogarUsuario = st.form_submit_button("Logar", use_container_width=True)
        
        if btnLogarUsuario:
            usuario = usuario.strip().lower()
            senha = senha.strip()
            
            if not usuario or not senha:
                st.error("Preencha usuário e senha.")
            else:
                ref = db.collection("usuarios").document(usuario)
                doc = ref.get()

                if not doc.exists:
                    st.error("Usuário não encontrado.")
                else:
                    dados = doc.to_dict()
                    if dados["senha"] == senha:
                        st.session_state.logado = True
                        st.session_state.usuario = usuario
                        st.session_state.role = dados.get("role", "cliente")
                        st.success("Login realizado!")
                    else:
                        st.error("Usuário ou senha incorretos.")

# Cadastro

if optionMenu == "Cadastrar":
    st.subheader("Cadastro:")

    with st.form("formLogar"):
        nome = st.text_input("Nome:", placeholder="Informe o seu nome..")
        usuario = st.text_input("Usuário:", placeholder="Informe seu usuário...")
        idade = st.number_input("Idade:", step=1, min_value=12, max_value=100)
        email = st.text_input("E-mail:", placeholder="Informe o seu e-mail...")
        senha = st.text_input("Senha:", placeholder="Informe a sua senha...", type="password")
        btnCadastrarUsuario = st.form_submit_button("Cadastrar", use_container_width=True)
        
        if btnCadastrarUsuario:
            usuario = usuario.strip().lower()

            if not nome or not usuario or not senha:
                st.error("Preencha todos os campos.")
            elif "@" not in email:
                st.error("Email inválido.")
            else:
                ref = db.collection("usuarios").document(usuario)

                if ref.get().exists:
                    st.error("Usuário já existe.")
                else:
                    ref.set({
                        "nome": nome,
                        "usuario": usuario,
                        "idade": idade,
                        "email": email,
                        "role": "cliente",
                        "senha": senha
                    })
                    st.success("Usuário cadastrado com sucesso")

            
# Editar

if optionMenu == "Editar Perfil":
    if not st.session_state.logado:
        st.warning("Faça login primeiro.")
    else:
        ref = db.collection("usuarios").document(st.session_state.usuario)
        dados = ref.get().to_dict()

        with st.form("formEditar"):
            nome = st.text_input("Nome", value=dados["nome"])
            idade = st.number_input("Idade", value=dados["idade"], step=1, min_value=12, max_value=100)
            senha = st.text_input("Nova senha", type="password")
            btn = st.form_submit_button("Salvar")

            if btn:
                ref.update({
                    "nome": nome,
                    "idade": idade,
                    "senha": senha if senha else dados["senha"]
                })
                st.success("Dados atualizados!")

# Recuperar senha

# é possível automatizar isso pelo email com o firebase, fazer se der tempo

if optionMenu == "Recuperar Senha":
    st.subheader("Recuperar Senha")

    usuario = st.text_input("Informe seu usuário")

    if st.button("Recuperar"):
        ref = db.collection("usuarios").document(usuario)
        doc = ref.get()

        if doc.exists:
            st.info(f"Sua senha é: {doc.to_dict()['senha']}")
        else:
            st.error("Usuário não encontrado")


# Sair

if st.session_state.logado:
    st.divider()
    if st.button("Sair"):
        st.session_state.logado = False
        st.session_state.usuario = None
        st.rerun()


#html_code = """
#    <footer>✨ Gioia Artes — onde cada ponto conta uma história. ✨</footer>
#"""
#st.markdown(html_code, unsafe_allow_html=True)

#Rodapé

st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)

st.markdown("""
<style>
footer {
    position: fixed;
    bottom: 0;
    width: 100%;
    text-align: center;
    padding: 10px;
    background-color: #gray;
    color: #555;
    font-size: 0.9rem;
    z-index: 100;
}
</style>

<footer>
✨ Gioia Artes — onde cada ponto conta uma história. ✨
</footer>
""", unsafe_allow_html=True)


########### 