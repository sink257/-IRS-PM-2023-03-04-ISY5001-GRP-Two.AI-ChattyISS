from tabnanny import filename_only
from flask import Flask, request, jsonify, send_file, make_response
import base64
import io
import json
from NUS_ISS_chatbot.chatbot import load_chain
from flask_cors import CORS

app = Flask("__name__")
CORS(app)

@app.route('/')
def hello_world():
    return "Welcome to ISS NUS Chatbot"


chain = load_chain()
@app.route('/api/chat/')
def chat():
    chat_history = []
    question = request.args.get('data') 
    print ("Received from caller: " + str(question))

    result = chain({"question": str(question), "chat_history": chat_history})
    responseMessage = result['answer']
     
    # If there is an image
    filename = 'image/sample.png'
    with open(filename, 'rb') as f:
        image_data = f.read()
    
    encoded_img = base64.b64encode(image_data).decode('utf-8')
    
    response = {'image':encoded_img, 'answer':responseMessage}

    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
