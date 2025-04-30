import streamlit as st
from openai import OpenAI
import os
from groq import Groq
import uuid

# Configurações da página
st.set_page_config(
    page_title="DecoGPT",
    page_icon="🤖",
    #layout="wide",
    initial_sidebar_state='expanded'
)

# Setup OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Setup Groq
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

clientgroq = Groq(
    api_key=GROQ_API_KEY,
)

# Selecionando o modelo que vai fazer a resposta
with st.sidebar:
    model = st.selectbox('Selecione o modelo', options=['deepseek-r1-distill-llama-70b',
                                                          'llama-3.3-70b-versatile',
                                                          'llama-3.1-8b-instant',
                                                          'llama3-8b-8192',
                                                          'meta-llama/llama-4-scout-17b-16e-instruct'])

# Criar função para retornar a mensagem do modelo
def retorna_resposta_modelo_groq(mensagens,
                                   api_key=GROQ_API_KEY,
                                   modelo=model,
                                   temperatura=0,
                                   stream=True):
    if modelo == 'deepseek-r1-distill-llama-70b':
        response = clientgroq.chat.completions.create(
            model=modelo,
            messages=mensagens,
            temperature=temperatura,
            stream=stream,
            reasoning_format="hidden"  # Adiciona o parâmetro para este modelo específico
        )
    else:
        response = clientgroq.chat.completions.create(
            model=modelo,
            messages=mensagens,
            temperature=temperatura,
            stream=stream
        )

    return response

# Função para armazenar a página principal
def pagina_principal():
    if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []

    mensagens = st.session_state['mensagens']

    st.header('Deco GPT', divider=True)

    # Adicionar uploader de arquivo
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload uma imagem", type=['png', 'jpg', 'jpeg'])

    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])

    # Input de texto do usuário
    prompt = st.chat_input('Fale com o chat')

    if uploaded_file:
        # Processar a imagem carregada
        image_url = f"https://upload.wikimedia.org/wikipedia/commons/f/f2/LPU-v1-die.jpg"

        # Criar mensagem multimodal
        nova_mensagem_imagem = {
            'role': 'user',
            'content': [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url
                    }
                }
            ]
        }

        # Adicionar mensagem à lista
        mensagens.append(nova_mensagem_imagem)
        st.session_state['mensagens'] = mensagens

        # Mostrar mensagem ao usuário
        chat = st.chat_message(nova_mensagem_imagem['role'])
        chat.markdown(str(nova_mensagem_imagem['content'][0]['text']))

        # Obter resposta do modelo
        chat = st.chat_message('assistant')
        placeholder = chat.empty()
        resposta_completa = ''

        respostas = retorna_resposta_modelo_groq([nova_mensagem_imagem], stream=True)

        for resposta in respostas:
            if resposta.choices[0].delta.content is not None:
                resposta_completa += str(resposta.choices[0].delta.content)
                placeholder.markdown(resposta_completa)

        if resposta_completa:
            nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
            mensagens.append(nova_mensagem)
            st.session_state['mensagens'] = mensagens

    if prompt:
        nova_mensagem = {'role': 'user', 'content': prompt}
        chat = st.chat_message(nova_mensagem['role'])
        chat.markdown(nova_mensagem['content'])
        mensagens.append(nova_mensagem)

        chat = st.chat_message('assistant')
        placeholder = chat.empty()
        resposta_completa = ''

        placeholder.markdown('| ')
        respostas = retorna_resposta_modelo_groq(mensagens,
                                                  stream=True)
        for resposta in respostas:
            if resposta.choices[0].delta.content is not None:
                resposta_completa += str(resposta.choices[0].delta.content)
                placeholder.markdown(resposta_completa)

        if resposta_completa:
            nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
            mensagens.append(nova_mensagem)

        st.session_state['mensagens'] = mensagens

pagina_principal()
