import streamlit as st
from openai import OpenAI
import os


# Setup OpenAI
OPENAI_API_KEY = st.text_input(label = 'API')

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

pagina_principal()
