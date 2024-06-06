import google.generativeai as genai
from datetime import date, datetime, timedelta
from docx import Document
import os

def ultimo_dia_util(data):
  data -= timedelta(days=1)
  while data.weekday() >= 5:
    data -= datetime.timedelta(days=1)
  return datetime.strftime(data,'%d/%m/%Y')

def extrair_procedimento(filename:str):
    try:
        doc = Document(filename)
        texto = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    except:
        texto = ''
        pass

    return texto
  
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

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
  system_instruction= """Sou assistente de secretária do time de PCP da WEG Energia."""
)

class SecretaryAI():
  def __init__(self):
    self.chat_session = model.start_chat()
  
  def send_message(self, path:str, filename:str):
    message = f"""
        Procedimento sobre {filename}:
        {extrair_procedimento(f'{path}')}
        Fim do procedimento;

        Baseado nas informações do acima, realize o comando abaixo:

        Substitua "ANO_ATUAL" por {date.today().year}, 
        Substitua "MES_ATUAL" por {date.today().month:02}, 
        Substitua "SEMANA_ATUAL" por {date.today().isocalendar().week}, 
        Substitua "ULTIMO_DIA_UTIL" por {ultimo_dia_util(date.today())}, 
        Substitua "DIA_ATUAL" por {date.today().day:02}
        Substitua "SEM_PASSADO" por {str(int(date.today().strftime('%m'))-1).zfill(2)};
        
        Formate as datas de 'LastUpdate' dos indicadores em formato de 'dd/mm/yyyy', mantendo a data que se encontra na base de dados.
        Separe o passo a passo para atualizar o indicador em vários tópicos;
"""
    response = self.chat_session.send_message(message).text
    return response.strip()
  

if __name__ == "__main__":
    procedure_path = "Q:\\GROUPS\\BR_SC_JGS_WM_LOGISTICA\\PCP\\PPC_AI_Procedures\\ppc_secretary\\daily\\Kanban diário JGS.docx"
    procedure_name = "Kanban diário JGS"
    ia = SecretaryAI()
    print(ia.send_message(procedure_path, procedure_name))
