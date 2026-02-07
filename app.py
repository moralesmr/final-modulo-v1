import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="Chatbot IMC",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ Chatbot de consulta de Indice de masa corporal y clasificación según OMS")
st.caption("Tambien puedes buscar artículos científicos relacionados a la temática - Este es un Asistente educativo, no reemplaza consulta médica!")

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ejemplos rápidos
st.markdown("### Ejemplos rápidos")
col1, col2 = st.columns(2)

with col1:
    if st.button("Ejemplo IMC"):
        st.session_state.input = "Mido 1.70 metros y peso 70 kg. ¿Cuál es mi IMC?"

with col2:
    if st.button("Ejemplo PubMed"):
        st.session_state.input = "Busca estudios recientes sobre IMC y obesidad."

prompt = st.chat_input("Escribí tu consulta")

if "input" in st.session_state:
    prompt = st.session_state.input
    del st.session_state.input

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Procesando..."):
            response = run_agent(prompt)
        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )
