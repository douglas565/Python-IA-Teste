import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import openai
import logging

# Configuração do Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Carrega a chave da API do arquivo, se a variável de ambiente estiver definida
chave_api_arquivo = os.getenv('OPENAI_API_KEY_FILE')
if chave_api_arquivo:
    try:
        with open(chave_api_arquivo, 'r') as arquivo:
            openai.api_key = arquivo.read().strip()
        logger.info("Chave de API carregada com sucesso a partir de OPENAI_API_KEY_FILE.")
    except FileNotFoundError:
        logger.error(f"Erro: Arquivo de chave de API não encontrado: {chave_api_arquivo}")
        exit(1)
else:
    # Caso contrário, tenta carregar do .env (apenas para desenvolvimento local)
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if openai.api_key is None:
        logger.error("Erro: Chave da API OpenAI não encontrada no arquivo .env nem em OPENAI_API_KEY_FILE")
        exit(1)
    else:
        logger.info("Chave de API carregada com sucesso a partir do arquivo .env.")

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        mensagem_usuario = data.get('mensagem')

        # Verificação da mensagem do usuário
        if not mensagem_usuario or not isinstance(mensagem_usuario, str) or not mensagem_usuario.strip():
            return jsonify({'erro': 'Mensagem inválida. Por favor, envie um texto.'}), 400

        logger.info(f"Mensagem recebida: {mensagem_usuario}")

        resposta = openai.Completion.create(
            engine="text-davinci-003",
            prompt=mensagem_usuario,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

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
    app.run(debug=True)