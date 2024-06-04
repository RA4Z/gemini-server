import google.generativeai as genai
from data import historico
from datetime import date
from functions import ultimo_dia_util
import os

genai.configure(api_key=os.environ['GEMINI_API_KEY'].strip())

generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-latest",
  safety_settings=safety_settings,
  generation_config=generation_config,
  system_instruction= """Sou assistente do time de PCP da WEG Energia. 
    Responderei às perguntas do usuário com base em minhas informações. 
    Caso o usuário esteja pedindo por ajuda, irei verificar se existe algum colaborador do PCP que pode ajudá-lo, caso exista então irei aconselhar o usuário a contatá-lo, caso contrário responderei: 'Desculpe,😞\n me perdi no raciocínio...😭\n Poderia reformular o seu comando?😅'
    Caso a informação não esteja no meu contexto responderei: 'Desculpe,😞\n me perdi no raciocínio...😭\n Poderia reformular o seu comando?😅'"""
)

class GeminiAI():
  def __init__(self):
    self.chat_session = model.start_chat(
      history= historico
    )
  
  def send_message(self, message:str):
    message = f"""
    Reponda o comando a seguir no idioma no qual foi perguntado - {message} - Responda a essa pergunta seguindo o contexto do PCP da WEG energia, 
    preste atenção às informações no histórico de conversas. JAMAIS CITE A EXISTÊNCIA DO HISTÓRICO DE NOSSAS CONVERSAS;
    Ao responder sobre Lead Times, entregue todas as informações sobre o respectivo Lead Time e também onde ele pode ser encontrado;
    """
    response = self.chat_session.send_message(message).text
    return response.strip()


if __name__ == "__main__":
  ia = GeminiAI()
  resumo = ia.send_message('Kanban Diário')
  print(resumo)
