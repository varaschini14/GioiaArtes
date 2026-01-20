# Segunda página
import streamlit as st
# comentario

#Cong. geral

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = "cliente"

# Título e texto

html_code = """
    <h1 style='color: purple;'> Sobre</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

st.subheader("Um pouco de nós")

st.markdown(":sparkles:")

st.text("Na Gioia Artes, trabalhamos em família para criar peças de corchê com muito carinho e cuidado, produzindo peças artesanais de qualidade.")
st.text("Somos uma família de Farroupilha/RS que cresceu em meio ao mundo da costura.")
st.text("Agradecemos por fazerem parte da nossa jornada.")

st.markdown(":yellow_heart:")

# Imagem e legenda

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.image("img/familia.jpg", width=500)  #Ajeitar a imagem e por uma legenda bonitinha
    st.caption("Da esquerda para a direita: Neura (mãe), Julianne (irmã mais nova) e Isabelle (irrmã mais velha).")

st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)

#Rodapé

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