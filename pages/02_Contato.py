# Segunda página
import streamlit as st
import requests
from streamlit_lottie import st_lottie

# comentario

#Config. geral

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = "cliente"

# Título

html_code = """
    <h1 style='color: purple;'> Contato</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

#Coluna insta e texto

st.subheader("Instagram")

col1, col2 = st.columns([1, 2])

with col1:
    def carregar_animacao(url: str):
        requisicao = requests.get(url)
        if requisicao.status_code != 200:
            return None
        return requisicao.json()

    url_animacao = "https://lottie.host/0bf17c36-4803-4b67-96c8-2f6717621ce9/HaPfbrDLpW.json"

    animacaoInsta = carregar_animacao(url_animacao)

    st_lottie(animacaoInsta, key="animacaoInsta", speed=1, loop=True, width=200)


with col2:
    st.space()
    st.space()
    st.text("Nos siga em:")
    st.markdown("[@gioiaartes](https://www.instagram.com/gioiaartes/)")


st.divider()

# Coluna email e texto

st.subheader("E-mail")

col1, col2 = st.columns([1, 2])

with col1:
    def carregar_animacao(url: str):
        requisicao = requests.get(url)
        if requisicao.status_code != 200:
            return None
        return requisicao.json()

    url_animacao = "https://lottie.host/f8973527-0029-45d0-b5cd-6054c91d5ce6/q4bjv7CGC0.json"

    animacaoEmail = carregar_animacao(url_animacao)

    st_lottie(animacaoEmail, key="animacaoEmail", speed=1, loop=True, width=200)


with col2:
    st.space()
    st.space()
    st.text("Converse conosco pelo e-mail: " \
    "\ngioiaartes@gmail.com")

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