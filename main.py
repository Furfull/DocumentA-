import streamlit as st
from node import graph
from services import chat_with_memory
from estruturaDefault import estrutura
import os

def create_readme(final_doc):
    with open("README.md", "w") as f:
        f.write(final_doc)
    return "README.md"

st.set_page_config(page_title="Document AÍ", page_icon="📄", layout="wide")
st.title("Document AÍ")

col1, col2 = st.columns([1, 3])

with col1:
    st.markdown("<br>", unsafe_allow_html=True)

    user_strutura = st.text_area("Estrutura", help="Este parâmetro é opcional")
    user_idioma = st.text_input("IDIOMA", help="Este parâmetro é opcional")

    uploaded_file = st.file_uploader("Escolha um arquivo", type=["py", "js", "go"], label_visibility="collapsed")
    
    if uploaded_file is not None and st.button("Gerar Documentação", use_container_width=True):
        state = {
            "file_path": uploaded_file,
            "code": "",
            "structure":  user_strutura if user_strutura else estrutura,
            "language": user_idioma if user_idioma else "pt-br",
            "documentation": "",
            "final_doc": "",
            "memory": [],
            "crag_analysis": "",
            "cont_errors": 0
        }
        with st.spinner("Gerando Documentação..."):
            final_state = graph.invoke(state)
            st.session_state.final_state = final_state 

        with open("README.md", "rb") as f:
            st.download_button(
                label="Baixar o README.md",
                data=f,
                file_name="README.md",
                mime="text/markdown",
                use_container_width=True
            )
        
    if st.button("🗑️"):
        state = {
            "file_path": None,
            "code": "",
            "structure": "",
            "language": "",
            "documentation": "",
            "final_doc": "",
            "memory": [],
            "crag_analysis": ""
        }
        if os.path.exists("README.md"):
            os.remove("README.md")
        st.success("Dados limpos e README.md excluído.")

with col2:
    st.subheader("Chat com a IA")
    container_2 = st.container(height=500)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        if message["role"] == "user":
            container_2.chat_message("user").markdown(f"**Você:** {message['content']}")
        else:
            container_2.chat_message("assistant").markdown(f"**Assistente:** {message['content']}")

    prompt = col2.chat_input("Pergunte algo sobre o código ou documentação:")

    if prompt:
        with st.spinner("Gerando Resposta..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            final_state = st.session_state.get("final_state")
            if final_state: 
                response = chat_with_memory(final_state, prompt)
                st.session_state.messages.append({"role": "assistant", "content": response})

                container_2.chat_message("user").markdown(f"**Você:** {prompt}")
                container_2.chat_message("assistant").markdown(f"**Assistente:** {response}")
            else:
                st.warning("Por favor, carregue um arquivo Python para começar.")

    else:
        st.warning("Por favor, carregue um arquivo Python para começar.")
