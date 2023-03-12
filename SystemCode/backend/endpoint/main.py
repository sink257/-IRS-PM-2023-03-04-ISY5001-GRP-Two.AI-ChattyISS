from tabnanny import filename_only
from flask import Flask, request, jsonify, send_file, make_response
import base64
import io

app = Flask("__name__")

@app.route('/')
def hello_world():
    return "Welcome to ISS NUS Chatbot"


@app.route('/api/chat/')
def chat():
    data = request.get_json() 
    question = data['question']
    print (question)

    responseMessage='Good question. i do not know'
    # If there is an image
    filename = 'image/sample.png'
    with open(filename, 'rb') as f:
        image_data = f.read()
    
    encoded_img = base64.b64encode(image_data).decode('utf-8')
    
    response = {'image':encoded_img, 'answer':responseMessage}

    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
