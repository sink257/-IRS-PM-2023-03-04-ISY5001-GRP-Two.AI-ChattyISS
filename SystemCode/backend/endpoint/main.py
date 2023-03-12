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
    responseMessage='Good question. i do not know'
    # If there is an image
    filename = 'image/sample.png'
    with open(filename, 'rb') as f:
        image_data = f.read()
    
    encoded_img = base64.b64encode(image_data).decode('utf-8')
    '''
    pil_image = Image.open(filename)
    image_response = send_file(filename, mimetype='image/png')
    with BytesIO() as buffer:
        image_response.save(buffer, 'PNG')
        response_bytes = buffer.getvalue()
    
    with open(filename, 'rb') as f:
        image_data = BytesIO(f.read())
        
    image_response = make_response(buffer.getvalue())
    image_response.headers.set('Content-Type','image/png')
    json_response = jsonify({'answer':responseMessage})
    response = make_response(image_response)
    response.set_data(json_response.get_data())
    '''
    response = {'image':encoded_img, 'answer':responseMessage}

    
    return jsonify(response)

if __name__ == '__main__':
    app.run()
