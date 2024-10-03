from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Configure sua chave de API da OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')
# Defina o modelo do ChatGPT que você deseja usar
modelo = "text-davinci-003" # ou outro modelo de sua preferência

@app.route('/chat', methods=['POST'])
def chat():
  try:
    dados = request.get_json()
    mensagem_usuario = dados.get('mensagem')

    if not mensagem_usuario:
      return jsonify({'erro': 'Mensagem não fornecida'}), 400

    resposta = openai.Completion.create(
      engine=modelo,
      prompt=mensagem_usuario,
      max_tokens=150, # Ajuste conforme necessário
      n=1,
      stop=None,
      temperature=0.7, # Ajuste a temperatura para respostas mais criativas (valores mais altos) ou mais conservadoras (valores mais baixos)
    )

    resposta_chatbot = resposta.choices[0].text.strip()
    return jsonify({'resposta': resposta_chatbot})

  except Exception as e:
    return jsonify({'erro': f'Erro ao processar a requisição: {str(e)}'}), 500

if __name__ == '__main__':
  app.run(debug=True, port=5000)