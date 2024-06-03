from gemini import GeminiAI
from flask import Flask, request

app = Flask(__name__)

@app.route('/gemini', methods=['POST'])
def process_message():
  message = request.form.get('message')
  if message:
    response = ia.send_message(message)
    return response
    
  else:
    return "Mensagem inválida", 400

if __name__ == "__main__":
  ia = GeminiAI()  # Inicialize a IA apenas uma vez
  app.run(host='0.0.0.0', port=5000) 