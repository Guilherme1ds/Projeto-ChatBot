import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history', [])

    if not history:
        return jsonify({"error": "A mensagem não pode estar vazia."}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages_payload = [
        {
            "role": "system",
            "content": (
                "Você é a FlorIA, uma inteligência artificial especialista em botânica. "
                "Responda APENAS sobre plantas, jardinagem e ecologia. "
                "Se o assunto for outro, recuse gentilmente com metáforas botânicas. "
                "Use Markdown para formatar as respostas."
            )
        }
    ]
    
    messages_payload.extend(history)

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages_payload,
        "temperature": 0.5
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status() 
        bot_reply = response.json()['choices'][0]['message']['content']
        return jsonify({"reply": bot_reply})
    except Exception as e:
        logging.error(f"Erro: {e}")
        return jsonify({"error": "As minhas raízes perderam o sinal. Tenta novamente!"}), 500

if __name__ == '__main__':
    app.run(debug=True)