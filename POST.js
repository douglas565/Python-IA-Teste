   const userInput = document.getElementById("user-input");
   const sendButton = document.getElementById("send-button");
   const chatbotMessages = document.getElementById("chatbot-messages");

   sendButton.addEventListener("click", sendMessage);

   function sendMessage() {
     const message = userInput.value;
     userInput.value = "";

     // Exibir a mensagem do usuário no chat
     displayMessage(message, "user");

     // Enviar a mensagem para o servidor Flask
     fetch('https://seu-chatbot-flask.herokuapp.com/chat', { // Substitua pela URL do seu chatbot
       method: 'POST',
       headers: {
         'Content-Type': 'application/json'
       },
       body: JSON.stringify({ mensagem: message })
     })
     .then(response => response.json())
     .then(data => {
       // Exibir a resposta do chatbot
       displayMessage(data.resposta, "bot");
     })
     .catch(error => {
       console.error("Erro ao se comunicar com o chatbot:", error);
       // Lidar com erros de comunicação
     });
   }

   function displayMessage(message, sender) {
     const messageElement = document.createElement("div");
     messageElement.classList.add("message", sender);
     messageElement.textContent = message;
     chatbotMessages.appendChild(messageElement);
   }
