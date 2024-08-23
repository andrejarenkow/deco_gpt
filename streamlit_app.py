import streamlit as st
from openai import OpenAI
import os

# Configurações da página
st.set_page_config(
    page_title="DecoGPT",
    page_icon="	:robot:",
    #layout="wide",
    #initial_sidebar_state='collapsed'
) 


# Setup OpenAI
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

client = OpenAI(
   api_key=OPENAI_API_KEY,
 )

# Criar função para retornar a mensagem do modelo
def retorna_resposta_modelo(mensagens,
                            openai_key = OPENAI_API_KEY,
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

import streamlit as st

# Função para armazenar a página principal
def pagina_principal():
    # Verifica se a chave 'mensagens' existe no st.session_state
   if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []  # Inicializa 'mensagens' como uma lista vazia

   mensagens = st.session_state['mensagens']  # Acessa a lista de mensagens

   st.header('Deco GPT', divider=True)

   for mensagem in mensagens:
      chat = st.chat_message(mensagem['role'])
      chat.markdown(mensagem['content'])

   prompt = st.chat_input('Fale com o chat')
   if prompt:
      nova_mensagem = {'role':'user', 'content':prompt}
      chat = st.chat_message(nova_mensagem['role'])
      chat.markdown(nova_mensagem['content'])
      mensagens.append(nova_mensagem)
      
      chat = st.chat_message('assistant')
      placeholder = chat.empty()
      resposta_completa = ''

      placeholder.markdown('| ')
      respostas = retorna_resposta_modelo(mensagens,
                                          stream=True)
      for resposta in respostas:
          # Verifica se o conteúdo da resposta não é None antes de concatenar
          if resposta.choices[0].delta.content is not None:
              resposta_completa += str(resposta.choices[0].delta.content)
              placeholder.markdown(resposta_completa + '| ')  # Atualiza o placeholder com o conteúdo parcial
      
      # Cria a nova mensagem apenas se houver conteúdo na resposta completa
      if resposta_completa:
          nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
          mensagens.append(nova_mensagem)

      st.session_state['mensagens'] = mensagens

pagina_principal()
