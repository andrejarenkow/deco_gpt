import streamlit as st
import os
from groq import Groq
from pandasai import SmartDataframe
import pandas as pd


# Configurações da página
st.set_page_config(
    page_title="PandasAI",
    page_icon="🤖",
    #layout="wide",
    initial_sidebar_state='expanded'
) 


# Setup Groq
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

clientgroq = Groq(
   api_key=GROQ_API_KEY,
 )

llm = ChatGroq(
    model_name="mixtral-8x7b-32768", 
    api_key = st.secrets["GROQ_API_KEY"]
)

# Importação dos dados
data = pd.read_csv("/content/escolas_estaduais.csv", sep = ';')
data

# Criar função para retornar a mensagem do modelo
def retorna_resposta_modelo_groq(mensagens,
                            api_key = GROQ_API_KEY,
                            modelo = 'llama3-8b-8192',
                            temperatura=0,
                            stream=True):
  response = clientgroq.chat.completions.create(
    model = modelo,
    messages = mensagens,
    temperature = temperatura,
    stream = stream
)
  return response



# Função para armazenar a página principal
def pagina_principal():
    # Verifica se a chave 'mensagens' existe no st.session_state
   if 'mensagens' not in st.session_state:
        st.session_state.mensagens = []  # Inicializa 'mensagens' como uma lista vazia

   mensagens = st.session_state['mensagens']  # Acessa a lista de mensagens

   st.header('Pandas AI', divider=True)

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
      respostas = retorna_resposta_modelo_groq(mensagens,
                                          stream=True)
      for resposta in respostas:
          # Verifica se o conteúdo da resposta não é None antes de concatenar
          if resposta.choices[0].delta.content is not None:
              resposta_completa += str(resposta.choices[0].delta.content)
              placeholder.markdown(resposta_completa)  # Atualiza o placeholder com o conteúdo parcial
      
      # Cria a nova mensagem apenas se houver conteúdo na resposta completa
      if resposta_completa:
          nova_mensagem = {'role': 'assistant', 'content': resposta_completa}
          mensagens.append(nova_mensagem)

      st.session_state['mensagens'] = mensagens

pagina_principal()
