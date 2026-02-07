import streamlit as st
from agent import run_agent

st.set_page_config(
    page_title="Chatbot IMC",
    page_icon="⚖️",
    layout="centered"
)

st.title("⚖️ Chatbot de IMC y PubMed")
st.caption("Asistente educativo — no reemplaza consulta médica")

modo = st.radio(
    "Modo:",
    ["📏 Calcular IMC", "📚 Buscar en PubMed"],
    horizontal=True
)

# Historial
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ejemplos
st.markdown("### Ejemplos rápidos")

if modo == "📏 Calcular IMC":
    if st.button("Ejemplo IMC"):
        st.session_state.input = "Mido 5.6 pies y peso 180 libras. Calculá mi IMC."
else:
    if st.button("Ejemplo PubMed"):
        st.session_state.input = "Busca estudios sobre IMC y obesidad."

prompt = st.chat_input("Escribí tu consulta")

if "input" in st.session_state:
    prompt = st.session_state.input
    del st.session_state.input

# Validación visual
def validar(texto):
    if modo == "📏 Calcular IMC":
        return "pie" in texto.lower() and "libra" in texto.lower()
    return True

if prompt:
    if not validar(prompt):
        st.warning("⚠️ Usa pies y libras para calcular IMC.")
    else:
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
