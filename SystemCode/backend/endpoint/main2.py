from tabnanny import filename_only
from flask import Flask, request, jsonify, render_template
import base64
import io
import json
from NUS_ISS_chatbot.chatbot import load_chain as load_chaingpt3_5
from NUS_ISS_chatbot.chatbot_gpt4 import load_chain as load_chaingpt4
from NUS_ISS_chatbot.understandimages import clearAndLoadTextTokensFromFile
from NUS_ISS_chatbot.understandimages import findSuitableImage2

from flask_cors import CORS

app = Flask("__name__")
CORS(app)

chat_history = []
text_tokens = {}
chain = load_chaingpt3_5()
global_parameter1 = "option1" # GPT4
global_parameter2 = "optionA" # Tesseract Model

@app.route('/', methods=['GET', 'POST'])
def index():
    global global_parameter1, global_parameter2, chain
    message = ""
    if request.method == 'POST':
        curr_parameter1 = global_parameter1
        curr_parameter2 = global_parameter2
        global_parameter1 = request.form.get('parameter1')
        global_parameter2 = request.form.get('parameter2')

        if global_parameter1 != curr_parameter1:
            if global_parameter1 == "option1":
                chain = None
                chain = load_chaingpt3_5()
                print ("option 1 is selected")
            if global_parameter1 == "option2" :
                chain = None
                chain = load_chaingpt4()
                print ("option 2 is selected")

        message = f"Parameters updated successfully. Parameter 1: {global_parameter1}, Parameter 2: {global_parameter2}"

    return render_template('index.html', message=message)



@app.route('/api/chat/')
def chat():

    question = request.args.get('data') 
    print ("Received from caller: " + str(question))

    
    result = chain({"question": str(question), "chat_history": chat_history})
    chat_history.append((question, result['answer']))
    responseMessage = result['answer']

    similarimage = findSuitableImage2(str(responseMessage), text_tokens)
    print(similarimage)
     
    # If there is an image
    filename = similarimage#'image/sample.png'
    encoded_img = ""

    if not filename:
        print("The filename is empty.")
    else:
        with open(filename, 'rb') as f:
            image_data = f.read()
            encoded_img = base64.b64encode(image_data).decode('utf-8')
    
    response = {'image':encoded_img, 'answer':responseMessage}

    
    return jsonify(response)

if __name__ == '__main__':
    text_tokens = clearAndLoadTextTokensFromFile()
    app.run()
