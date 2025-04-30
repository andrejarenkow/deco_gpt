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

# Função para gerar áudio a partir de texto
def gerar_audio(texto):
    try:
        # Configurações para o modelo de TTS
        model = "playai-tts"
        voice = "Fritz-PlayAI"  # Você pode escolher outras vozes disponíveis
        response_format = "wav"

        response = clientgroq.audio.speech.create(
            model=model,
            voice=voice,
            input=texto,
            response_format=response_format
        )

        # Gera um nome único para o arquivo
        filename = f"speech_{uuid.uuid4()}.wav"
        response.write_to_file(filename)

        return filename

    except Exception as e:
        st.error(f"Erro ao gerar áudio: {str(e)}")
        return None

# Selecionando o modelo que vai fazer a resposta
with st.sidebar:
    model = st.selectbox('Selecione o modelo', options=['deepseek-r1-distill-llama-70b',
                                                          'llama-3.3-70b-versatile',
                                                          'llama-3.1-8b-instant',
                                                          'llama3-8b-8192'])

# Criar função para retornar a mensagem do modelo
def retorna_resposta_modelo_groq(mensagens,
                            api_key=GROQ_API_KEY,
                            modelo=model,
                            temperatura=0,
                            stream=True):
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

    for mensagem in mensagens:
        chat = st.chat_message(mensagem['role'])
        chat.markdown(mensagem['content'])

    prompt = st.chat_input('Fale com o chat')
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

            # Gera o áudio da resposta
            audio_file = gerar_audio(resposta_completa)

            if audio_file:
                # Cria um player de áudio
                st.audio(audio_file, format='audio/wav')

                # Opcional: Ofereça a opção de download
                with open(audio_file, "rb") as audio_file:
                    st.download_button(
                        label="Download do áudio",
                        data=audio_file,
                        file_name=audio_file.name,
                        mime="audio/wav"
                    )

        st.session_state['mensagens'] = mensagens

pagina_principal()
