# Setup OpenAI

from openai import OpenAI
import os
OPENAI_API_KEY = ''

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
