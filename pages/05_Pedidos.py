import streamlit as st
from google.cloud import firestore

st.set_page_config(page_title="Finalizar Compra", layout="wide")

# Proteção

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = "cliente"

if "usuario" not in st.session_state or st.session_state.usuario is None:
    st.error("Você precisa estar logado.")
    st.stop()

#Busca os dados

usuario_id = st.session_state.usuario
key_dict = dict(st.secrets["firebase"])
db = firestore.Client.from_service_account_info(key_dict)

#Título e infos

html_code = """
    <h1 style='color: purple;'> Finalizar Compra</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

compras_ref = (
    db.collection("usuarios")
      .document(usuario_id)
      .collection("compras")
      .stream()
)

compras = list(compras_ref)

if len(compras) == 0:
    st.info("Seu carrinho está vazio.")
    st.stop()

total = 0

for compraRef in compras:
    compra = compraRef.to_dict()
    produto = compra.get("produto")
    preco = compra.get("preco", 0)

    total += preco
    st.write(f"🧶 {produto} — R$ {preco:.2f}")

    st.divider()

#Apresenta o total e métodos de pagamento

st.subheader(f"Total a pagar: R$ {total:.2f}")

st.divider()

st.subheader("Pagamento via Pix")

st.write("Utilize a chave Pix abaixo para realizar o pagamento:")
st.code("chave-pix-gioia-artes@email.com")

st.info("Após o pagamento, sua compra será confirmada manualmente.")

#Confirma o pagamento e permite que a compra seja enviada para o administrador

if st.button("💳 Confirmar pagamento"):
    for compraRef in compras:
        compraRef.reference.update({
            "status": "pago"
        })

    st.success("Pagamento confirmado! Aguarde a produção.")

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