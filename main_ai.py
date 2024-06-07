from gemini_chatbot import GeminiAI
from gemini_search_folders import SearchFoldersAI
from gemini_secretary_prompt import SecretaryAI

from functions import input_history
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Dicionário para armazenar os objetos GeminiAI para cada usuário
user_ias = {}

@app.route('/gemini', methods=['POST'])
def process_message():
  message = request.form.get('message')
  username = request.form.get('username')
  
  if message:
    # Crie um novo objeto GeminiAI se o usuário não existir
    if username not in user_ias:
      user_ias[username] = GeminiAI() 

    response = user_ias[username].send_message(message)

    try:
      input_history(username, message, response)
    except Exception as e:
      print(str(e))
      
    return response
  else:
    return "Mensagem inválida", 400


@app.route('/quit', methods=['POST'])
def quit_system():
  username = request.form.get('username')

  if username in user_ias:
    try:
      del user_ias[username] 
      return f'Usuário {username} deletado com sucesso!'

    except Exception as e:
      print(str(e))

  return 'Usuário inexistente'

@app.route('/search', methods=['POST'])
def search_file():
  search = SearchFoldersAI()
  message = request.form.get('message')

  if message:
    response = search.send_message(message)
    return response
  
  else:
    return "Mensagem inválida", 400
  
@app.route('/secretary', methods=['POST'])
def search_secretary_procedure():
  search = SecretaryAI()
  path = request.form.get('path')
  filename = request.form.get('filename')

  if filename:
    response = search.send_message(path, filename)
    return response
  
  else:
    return "Mensagem inválida", 400
  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)