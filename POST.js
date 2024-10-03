fetch('/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ mensagem: 'Olá, chatbot!' })
  })
  .then(response => response.json())
  .then(data => {
    console.log(data.resposta); // Exibe a resposta do chatbot
  });