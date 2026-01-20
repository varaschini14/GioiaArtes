# Alterar o for a seguir para mostrar na página de cadastro e fazer mais mudanças.

import streamlit as st
from google.cloud import firestore
from datetime import datetime
# depois adicionar a forma certa de data

#Estado do usuário

if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = "cliente"

if "usuario" not in st.session_state:
    st.error("Você precisa estar logado para ver suas compras.")
    st.stop()

#Busca os dados

usuario_id = st.session_state.usuario
key_dict = dict(st.secrets["firebase"])
db = firestore.Client.from_service_account_info(key_dict)

#Apresneta as compras

compras_ref = (
    db.collection("usuarios")
      .document(usuario_id)
      .collection("compras")
      .stream()
)

compras = list(compras_ref)
quantidade = len(compras)

#soma a qnt de compras

st.header(f"🛒 Carrinho ({quantidade})")

if len(compras) == 0:
    st.info("Não há produtos no carrinho.")
else:
    for compraRef in compras:
        compras = compraRef.to_dict()

        produto = compras.get("produto", "Produto desconhecido")
        preco = compras.get("preco", 0)
        data = compras.get("data", "-")
        status = compras.get("status", "-")

        col1, col2 = st.columns([4, 1])

        with col1:
            st.subheader(f"🧶 {produto}")
            st.write(f":material/payments: Preço: R$ {preco}")
            st.write(f":material/event: Data: {data}")
            st.write(f":material/local_shipping: Status: {status}")

        with col2:
            if st.button("Remover", key=f"remover_{compraRef.id}"):
                compraRef.reference.delete()
                st.success("Produto removido do carrinho!", icon="🗑️",)
        st.divider()

if quantidade > 0:
    if st.button("✅ Finalizar compra", use_container_width=True):
        st.switch_page("pages/05_Pedidos.py")

        if st.button("🛍️ Confirmar compra", use_container_width=True):
            for compraRef in compras:
                db.collection("usuarios") \
                  .document(usuario_id) \
                  .collection("historico_compras") \
                .add(compraRef.to_dict())

                compraRef.reference.delete()

            st.success("Compra finalizada! Carrinho limpo com sucesso.")

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