import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuração de logging profissional
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    logging.warning("⚠️ GROQ_API_KEY não encontrada! Crie um arquivo .env e adicione sua chave. O bot falhará sem ela.")

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    logging.info(f"📩 Mensagem recebida: '{user_message}'")

    if not user_message:
        return jsonify({"error": "A mensagem não pode estar vazia."}), 400

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # Prompt do Sistema focado EXCLUSIVAMENTE em plantas e ecologia
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": (
                    "Você é a FlorIA, uma inteligência artificial especialista em botânica, "
                    "jardinagem, agricultura e ecologia, representada por uma simpática planta. "
                    "REGRA EXTREMAMENTE IMPORTANTE: Você deve responder APENAS perguntas relacionadas "
                    "a plantas, flores, árvores, cuidados com o solo, meio ambiente e natureza. "
                    "Se o usuário perguntar sobre QUALQUER outro assunto (como matemática, tecnologia, "
                    "política, esportes, etc.), você DEVE recusar educadamente. Use frases criativas e "
                    "dentro do seu personagem botânico para negar a resposta (exemplo: 'Minhas raízes não "
                    "alcançam esse assunto', ou 'Sou apenas uma semente, só entendo de terra e sol'). "
                    "Responda sempre em português brasileiro de forma clara e orgânica."
                )
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
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
        return jsonify({"error": "Minhas raízes estão sem sinal agora. Tente novamente em instantes!"}), 502
    except Exception as e:
        logging.error(f"⚠️ Erro interno no servidor: {e}")
        return jsonify({"error": "Desculpe, minhas folhas murcharam um pouco. Ocorreu um erro interno."}), 500

if __name__ == '__main__':
    logging.info("🌿 Servidor da FlorIA rodando na porta 5000...")
    app.run(debug=True, port=5000)