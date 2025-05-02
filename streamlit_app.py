import streamlit as st
import os
from groq import Groq
import uuid

# Configurações da página
st.set_page_config(
    page_title="DecoGPT",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state='expanded'
)

# Setup Groq
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

clientgroq = Groq(
    api_key=GROQ_API_KEY,
)

# Modelo padrão
DEFAULT_MODEL = 'llama-3.1-8b-instant'

def get_model_parameters(model_name):
    """Retorna parâmetros específicos para cada modelo."""
    params = {
        'deepseek-r1-distill-llama-70b': {'reasoning_format': 'hidden'},
        'llama-3.3-70b-versatile': {},
        'llama-3.1-8b-instant': {},
        'llama3-8b-8192': {},
        'meta-llama/llama-4-scout-17b-16e-instruct': {}
    }
    return params.get(model_name, {})

def retorna_resposta_modelo_groq(mensagens, model_name, temperatura=0, stream=True):
    """Retorna a resposta do modelo Groq."""
    params = get_model_parameters(model_name)

    try:
        response = clientgroq.chat.completions.create(
            model=model_name,
            messages=mensagens,
            temperature=temperatura,
            stream=stream,
            **params
        )
        return response
    except Exception as e:
        st.error(f"Erro ao obter resposta do modelo: {str(e)}")
        return None

def pagina_principal():
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    mensagens = st.session_state['mensagens']

    st.header('Deco GPT', divider=True)

    # Exibe as mensagens anteriores
    for mensagem in mensagens:
        with st.chat_message(mensagem['role']):
            st.markdown(mensagem['content'])

    # Input do usuário
    prompt = st.chat_input('Fale com o chat')

    if prompt:
        nova_mensagem = {'role': 'user', 'content': prompt}
        mensagens.append(nova_mensagem)
        st.session_state['mensagens'] = mensagens

        # Exibe a resposta do assistente
        with st.chat_message('assistant'):
            placeholder = st.empty()

            try:
                respostas = retorna_resposta_modelo_groq(
                    mensagens,
                    model_name=model,
                    temperatura=0,
                    stream=True
                )

                resposta_completa = ''
                for resposta in respostas:
                    if resposta.choices[0].delta.content:
                        resposta_completa += resposta.choices[0].delta.content
                        placeholder.markdown(resposta_completa)

                if resposta_completa:
                    nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
                    mensagens.append(nova_mensagem)
                    st.session_state['mensagens'] = mensagens

            except Exception as e:
                st.error(f"Erro ao processar resposta: {str(e)}")

def main():
    # Selecionando o modelo que vai fazer a resposta
    with st.sidebar:
        st.header("Configurações")
        #global model
        model = st.selectbox(
            'Selecione o modelo',
            options=[
                'deepseek-r1-distill-llama-70b',
                'llama-3.3-70b-versatile',
                'llama-3.1-8b-instant',
                'llama3-8b-8192',
                'meta-llama/llama-4-scout-17b-16e-instruct'
            ],
            default=DEFAULT_MODEL
        )

        temperatura = st.slider(
            "Temperatura",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.1
        )

        if st.button("Limpar conversa"):
            st.session_state.mensagens = []
            st.experimental_rerun()

    pagina_principal()

if __name__ == "__main__":
    main()
