import streamlit as st
from google.cloud import firestore
from streamlit_option_menu import option_menu

#Estado do usuário, ou seja, permite apenas admins

if "logado" not in st.session_state or not st.session_state.logado:
    st.error("Acesso negado.")
    st.stop()

if st.session_state.role != "admin":
    st.error("Você não tem permissão para acessar esta página.")
    st.stop()

# Título

html_code = """
    <h1 style='color: purple;'> Painel Administrativo</h1>
"""
st.markdown(html_code, unsafe_allow_html=True)

# Busca dados

key_dict = dict(st.secrets["firebase"])
db = firestore.Client.from_service_account_info(key_dict)
compras = db.collection_group("compras").stream()
usuario_id = st.session_state.usuario

# Menu

optionMenu = option_menu(
    menu_title="Menu",
    options=["Pedidos Pendentes","Adicionar Produto","Editar ou Excluir Produtos"],
    icons=["box-seam","plus-circle","pencil-square"],
    menu_icon=["palette"],
    default_index=0
)

# Lista os pedidos feitos e o cliente

if optionMenu == "Pedidos Pendentes":

    st.subheader("Pedidos realizados por clientes:")

    pedidos = list(
        db.collection_group("compras")
          .where("status", "==", "pago")
          .stream()
    )  
    if len(pedidos) == 0:
        st.info("Não há pedidos pendentes no momento.")
    
    else:
        for pedido in pedidos:
            dados = pedido.to_dict()
            pedido_id = pedido.id
            pedido_ref = pedido.reference

            nome = dados.get("usuario_nome", "Cliente desconhecido")
            produto = dados.get("produto", "-")
            email = dados.get("email","-")
            status = dados.get("status", "-")

            col1, col2 = st.columns([4,1])
            with col1:
                st.markdown(f"""
                👤 **Cliente:** {nome}  
                🧶 **Produto:** {produto} 
                📧 **Email:** {dados['usuario_email']}  
                📦 **Status:** {status}
                """)
                st.divider()
    
        with col2:
            if st.button(
                "Fabricado",
                key=f"fabricado_{pedido_id}"
            ):
                pedido_ref.update({
                    "status": "fabricado"
                })
                st.success("Pedido marcado como fabricado!")
                st.rerun()

# Permite, atraves e form, adicionar produtos

if optionMenu == "Adicionar Produto":

    st.subheader("Adicionar um produto novo:")

    with st.form("novo_produto"):
        nome = st.text_input("Nome", placeholder="Informe o seu nome...")
        preco = st.number_input("Preço", placeholder="Informe o preço do produto...",min_value=0.0)
        descricao = st.text_area("Descrição", placeholder="Insira uma breve descrição do produto...")
        imagem = st.file_uploader(
            label="Escolha uma imagem",
            type=["jpg","jpeg","png"],)
        
        salvar = st.form_submit_button("Salvar")

        if salvar:
            caminho = None
            if imagem:
                caminho = f"img/{imagem.name}"
                with open(caminho, "wb") as f:
                    f.write(imagem.getbuffer())

            db.collection("produtos").add({
                "nome": nome,
                "preco": preco,
                "descricao": descricao,
                "imagem": caminho
            })

            st.success("Produto adicionado!")
            st.rerun()


# Permite, através de form, editar ou excluir

if optionMenu == "Editar ou Excluir Produtos":

    st.subheader("Editar ou excluir produtos já existentes:")

    produtos_ref = db.collection("produtos").stream()

    for produtoRef in produtos_ref:
        produto_id = produtoRef.id
        produto = produtoRef.to_dict()

        st.subheader(produto["nome"])
        st.write(f"R$ {produto['preco']:.2f}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Editar", key=f"edit_{produto_id}"):
                st.session_state.produto_editando = produto_id

        with col2:
            if st.button("Excluir", key=f"del_{produto_id}"):
                db.collection("produtos").document(produto_id).delete()
                st.warning("Produto removido!")
                st.rerun()

    if "produto_editando" in st.session_state:
        produto_ref = db.collection("produtos").document(st.session_state.produto_editando)
        dados = produto_ref.get().to_dict()

        st.subheader("Editar produto")

        with st.form("editar_produto"):
            nome = st.text_input("Nome", value=dados["nome"])
            preco = st.number_input("Preço", value=dados["preco"])
            salvar = st.form_submit_button("Salvar")

            if salvar:
                produto_ref.update({
                    "nome": nome,
                    "preco": preco
                })
                st.success("Produto atualizado!")
                del st.session_state.produto_editando
                st.rerun()

# Rodapé

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