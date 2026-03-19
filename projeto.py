from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) 

GROQ_API_KEY = "sua_chave_aqui"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    print(f"📩 Mensagem recebida do HTML: '{user_message}'")

    if not user_message:
        return jsonify({"error": "A mensagem chegou vazia ao backend!"}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "Você é a FlorIA, uma inteligência artificial amigável representada por uma planta. Responda em português brasileiro de forma prestativa, clara e simpática."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        
        if not response.ok:
            print(f"❌ Erro da Groq: {response.text}")
            
        response.raise_for_status() 
        
        response_data = response.json()
        bot_reply = response_data['choices'][0]['message']['content']
        
        return jsonify({"reply": bot_reply})
        
    except Exception as e:
        print(f"⚠️ Erro no servidor: {e}")
        return jsonify({"error": "Desculpe, as minhas folhas murcharam um pouco. Erro ao conectar com o cérebro da FlorIA."}), 500

if __name__ == '__main__':
    print("🌿 Servidor da FlorIA rodando na porta 5000...")
    app.run(debug=True, port=5000)