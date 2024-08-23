import streamlit as st
from openai import OpenAI
import os


# Setup OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
   api_key=OPENAI_API_KEY,
 )

# Criar função para retornar a mensagem do modelo
def retorna_resposta_modelo(mensagens,
                            openai_key,
                            modelo = 'gpt-4o-mini',
                            temperatura=0,
                            stream=False):
  response = client.chat.completions.create(
    model = modelo,
    messages = mensagens,
    temperature = temperatura,
    stream = stream
)
  return response

# Função para armazenar a página principal
def pagina_principal():

   if not 'mensagens' in st.session_state:
      st.session_state.mensagens = []

   mensagens = st.session_state['mensagens']
   
   st.header('Deco GPT', divider = True)
   
   for mensagem in mensagens:
      chat = st.chat_message(mensagem['role'])
      chat.markdown(mensagem['content'])

   prompt = st.chat_input('Fale com o chat')
   if prompt:
      nova_mensagem = {'role':'user', 'content':prompt}
      chat = st.chat_message(nova_mensagem['role'])
      chat.markdown(nova_mensagem['content'])
      mensagens.append(nova_mensagem)
      st.session_state['mensagens'] = mensagens

pagina_principal()
