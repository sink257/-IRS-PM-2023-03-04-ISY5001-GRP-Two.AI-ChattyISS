const chatBody = document.querySelector('.chat-body');
const inputMessage = document.querySelector('.input-message');

function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
    const divElement = document.getElementById('messages-container');
    divElement.innerHTML = '';
}

async function submitForm(event) {
    event.preventDefault(); // Prevent form from submitting

    const formData = new FormData(event.target); // Get form data
    const message = formData.get('msg'); // Get message from form data

    // Do something with message, such as sending it to a server using fetch or an API
    console.log(message);
    addQuestionMessage(message, 'question')

    const json_data = JSON.stringify({ "question": message });
    const encoded_data = encodeURIComponent(json_data);
    
    const response = await fetch(`http://127.0.0.1:5000/api/chat/?data=${encoded_data}` , {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    
    const data = await response.json(); // Parse response JSON
    if (response.ok) {
        const answer = data.answer;
        const image_base64 = data.image;

        // Use 'answer' and 'image_base64' as needed
        // For example:
        console.log("Answer:", answer);
        console.log("Image (base64):", image_base64);

        addAnswerMessage(answer, 'bot');
        addAnswerImage(image_base64, 'bot')
    }
    else {
        addAnswerMessage('Error: Unable to fetch response', 'bot');
    }


    // Reset form
    event.target.reset();
}





function addQuestionMessage(text, sender) {
  const messages = document.getElementById('messages-container');
  const messageElement = document.createElement('div');
  messageElement.classList.add('question');
  messageElement.textContent = text;
  messages.appendChild(messageElement);

  // Scroll to the bottom of the messages container
  messages.scrollTop = messages.scrollHeight;
}

function addAnswerMessage(text, sender) {
    const messages = document.getElementById('messages-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('answer');
    messageElement.textContent = text;
    messages.appendChild(messageElement);

    // Scroll to the bottom of the messages container
    messages.scrollTop = messages.scrollHeight;
}

function addAnswerImage(image_base64, sender) {
    const messages = document.getElementById('messages-container');
    const messageElement = document.createElement('div');
    messageElement.classList.add('answer');

    const imageElement = document.createElement('img');
    imageElement.src = `data:image/png;base64,${image_base64}`;
    imageElement.alt = 'Answer image';
    imageElement.style.maxWidth = '100%'; // Optional, to ensure the image fits the container

    imageElement.addEventListener('click', () => {
        imageElement.classList.toggle('enlarged');
    });


    messageElement.appendChild(imageElement);
    messages.appendChild(messageElement);

    // Scroll to the bottom of the messages container
    messages.scrollTop = messages.scrollHeight;
}


