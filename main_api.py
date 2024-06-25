from gemini_chatbot import GeminiAI
from gemini_search_folders import SearchFoldersAI
from gemini_secretary_prompt import SecretaryAI

import json
from functions import input_history
from flask import Flask, request, jsonify
from flask_cors import CORS
from update_indicators import update

app = Flask(__name__)
CORS(app)

# Dicionário para armazenar os objetos GeminiAI para cada usuário
user_ias = {}
update()

@app.route('/gemini', methods=['POST'])
def process_message():
    message = request.form.get('message')
    username = request.form.get('username')
    if 'SITE' in username: username = request.remote_addr
    
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
    if 'SITE' in username: username = request.remote_addr

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


@app.route('/wen_indicators')
def get_wen_indicators():
    try:
        data = json.load(open("indicators/data/indicadores.json", "r", encoding="utf-8"))
        return jsonify(data)
    except Exception as e:
        print(str(e))
        return []

@app.route('/wen_database')
def get_wen_database():
    try:
        data = json.load(open("indicators/data/dados.json", "r", encoding="utf-8"))
        return jsonify(data)
    except Exception as e:
        print(str(e))
        return []

@app.route('/update')
def update_api():
    try:
        update()
        return
    except Exception as e:
        print(str(e))
        return


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
