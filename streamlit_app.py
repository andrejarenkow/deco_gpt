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
   st.header('Deco GPT', divider = True)

   #Mensagens exemplo
   mensagens = [{'role': 'user', 'content': 'O que´e uma maçã em cinco palavras?'},
                {'role': 'assistant', 'content': 'Fruta, saudável, doce, crocante, nutritiva.'},
                {'role': 'user', 'content': 'E qual é o seu tamanho?'}]
   
   for mensagem in mensagens:
      chat = st.chat_message(mensagem['role'])
      chat.markdown(mensagem.content)

pagina_principal()
