import streamlit as st
from groq import Groq

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Chat con Groq", page_icon="🤖")

st.title("🤖 Chat con Groq")
st.caption("Una aplicación de chat que usa los modelos de lenguaje de Groq.")

with st.sidebar:
    st.header("Configuración")
    modelo_elegido = st.selectbox(
        "Elige un modelo:",
        ("llama3-8b-8192", "mixtral-8x7b-32768", "gemma-7b-it")
    )

# --- FUNCIONES PRINCIPALES ---

def crear_cliente_groq():
    """Crea y devuelve un cliente de Groq usando la API Key guardada en st.secrets."""
    try:
        api_key = st.secrets["GROQ_API_KEY"]
        return Groq(api_key=api_key)
    except Exception:
        st.error("No se encontró la GROQ_API_KEY. Asegúrate de haberla configurado en tu archivo .streamlit/secrets.toml")
        st.stop()

def obtener_respuesta_modelo(cliente, modelo, historial_chat):
    """Envía el historial del chat al modelo de Groq y devuelve la respuesta generada."""
    try:
        chat_completion = cliente.chat.completions.create(
            messages=historial_chat,
            model=modelo,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error al comunicarse con la API de Groq: {e}")
        return None

# --- LÓGICA PRINCIPAL DE LA APLICACIÓN ---

cliente = crear_cliente_groq()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("El asistente está pensando..."):
        respuesta_ia = obtener_respuesta_modelo(cliente, modelo_elegido, st.session_state.messages)
    
    if respuesta_ia:
        st.session_state.messages.append({"role": "assistant", "content": respuesta_ia})
        with st.chat_message("assistant"):
            st.markdown(respuesta_ia)