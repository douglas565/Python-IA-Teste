import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import logging

# Carregando as variáveis de ambiente do arquivo .env
load_dotenv() 

# Configuração do Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Obtendo a chave da API OpenAI do arquivo .env
openai.api_key = open(os.getenv('OPENAI_API_KEY_FILE')).read().strip()

# Verificação da chave da API
if openai.api_key is None:
    logger.error("Erro: Chave da API OpenAI não encontrada no arquivo .env")
    exit(1)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensagem_usuario = data.get('mensagem')

        # Verificação da mensagem do usuário
        if not mensagem_usuario or not isinstance(mensagem_usuario, str) or not mensagem_usuario.strip():
            return jsonify({'erro': 'Mensagem inválida. Por favor, envie um texto.'}), 400

        logger.info(f"Mensagem recebida: {mensagem_usuario}")

        # Requisição para a API do OpenAI
        resposta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=mensagem_usuario,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extraindo a resposta do chatbot
        resposta_chatbot = resposta.choices[0].text.strip()
        logger.info(f"Resposta do chatbot: {resposta_chatbot}")

        return jsonify({'resposta': resposta_chatbot})

    except openai.error.OpenAIError as e:
        logger.error(f"Erro na API do OpenAI: {e}")
        return jsonify({'erro': 'Ocorreu um erro ao processar a requisição.'}), 500

    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        return jsonify({'erro': 'Ocorreu um erro inesperado.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)