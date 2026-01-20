# Terceira página
import streamlit as st
import json
from google.cloud import firestore

# Estado do usuário
if "usuario" not in st.session_state:
    st.session_state.usuario = None

if "logado" not in st.session_state:
    st.session_state.logado = False

if "role" not in st.session_state:
    st.session_state.role = "cliente"

#Título e texto

html_code = """
    <h1 style='color: purple;'> Produtos</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

st.text("Aqui você pode visualizar e comprar os nossos produtos!")
st.divider()

#Produtos e infos chamados no banco de dados

key_dict = dict(st.secrets["firebase"])
db = firestore.Client.from_service_account_info(key_dict)

# Carregar produtos
#with open("data/produtos.json", "r", encoding="utf-8") as f:
#    produtos = json.load(f)
#for produto in produtos:
#    db.collection("produtos").add(produto)

produtos_ref = db.collection("produtos").stream()
produtos = []

for p in produtos_ref:
    item = p.to_dict()
    item["id"] = p.id
    produtos.append(item)

#Loop que mostra os produtos, fotos e infos

for produto in produtos:
    col1, col2 = st.columns([1, 2])

#Carrossel
    with col1:
        imagens = produto["imagem"]

        # índice único por produto
        index_key = f"img_index_{produto['id']}"
        if index_key not in st.session_state:
            st.session_state[index_key] = 0

        st.image(
            imagens[st.session_state[index_key]],
            width=180
        )

        col_prev, col_next = st.columns(2)

        with col_prev:
            if st.button("⬅️", key=f"prev_{produto['id']}"):
                st.session_state[index_key] = (
                    st.session_state[index_key] - 1
                ) % len(imagens)

        with col_next:
            if st.button("➡️", key=f"next_{produto['id']}"):
                st.session_state[index_key] = (
                    st.session_state[index_key] + 1
                ) % len(imagens)

#Dados
    with col2:
        st.subheader(produto["nome"])
        st.write(produto["descricao"])
        st.write(f"R$ {produto['preco']:.2f}")

        if st.button("Comprar", key=f"produto_{produto['id']}"):

            if st.session_state.usuario is None:
                st.warning("Faça login para comprar.")
                st.stop()

            usuario_id = st.session_state.usuario

#Procura os dados do cliente e linka com a compra
            usuario_doc = (
                db.collection("usuarios")
                  .document(usuario_id)
                  .get()
            )

            if not usuario_doc.exists:
                st.error("Usuário inválido.")
                st.stop()

            usuario = usuario_doc.to_dict()

            db.collection("usuarios") \
              .document(usuario_id) \
              .collection("compras") \
              .add({
                "produto": produto["nome"],
                "preco": produto["preco"],
                "status": "no carrinho", 
                "produto_id": produto["id"],
                "usuario_id": usuario_id,
                "usuario_nome": usuario["nome"],
                "usuario_email": usuario["email"]
            })

            st.success("Produto adicionado ao carrinho!")

#não tá funcionando o aviso
    st.divider()

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