from gemini_chatbot import GeminiAI
from functions import input_history
from flask import Flask, request

app = Flask(__name__)

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

  
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)