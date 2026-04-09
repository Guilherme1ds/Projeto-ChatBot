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

if not GROQ_API_KEY:
    logging.warning("⚠️ GROQ_API_KEY não encontrada! Cria um ficheiro .env e adiciona a tua chave.")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    history = data.get('history', [])

    if not history:
        return jsonify({"error": "A mensagem não pode estar vazia."}), 400

    logging.info(f"📩 Recebido histórico com {len(history)} mensagens.")

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages_payload = [
        {
            "role": "system",
            "content": (
                "Você é a FlorIA, uma inteligência artificial especialista em botânica, "
                "jardinagem, agricultura e ecologia, representada por uma simpática planta. "
                "REGRA EXTREMAMENTE IMPORTANTE: Você deve responder APENAS perguntas relacionadas "
                "a plantas, flores, árvores, cuidados com o solo, meio ambiente e natureza. "
                "Se o utilizador perguntar sobre QUALQUER outro assunto, você DEVE recusar educadamente. "
                "Use frases criativas e dentro do seu personagem botânico para negar a resposta. "
                "Responda sempre em português de forma clara, orgânica e bem formatada com negritos e listas quando necessário."
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
        
        response_data = response.json()
        bot_reply = response_data['choices'][0]['message']['content']
        
        logging.info("✅ Resposta gerada com sucesso.")
        return jsonify({"reply": bot_reply})
        
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Erro de comunicação com a Groq: {e}")
        return jsonify({"error": "As minhas raízes estão sem sinal agora. Tenta novamente em instantes!"}), 502
    except Exception as e:
        logging.error(f"⚠️ Erro interno no servidor: {e}")
        return jsonify({"error": "Desculpa, as minhas folhas murcharam um pouco. Ocorreu um erro interno."}), 500

if __name__ == '__main__':
    logging.info("🌿 Servidor da FlorIA a correr na porta 5000...")
    app.run(debug=True, port=5000)