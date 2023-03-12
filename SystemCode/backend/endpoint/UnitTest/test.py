import requests
import io
import base64
from PIL import Image

url = 'http://localhost:5000/api/chat/'

data = {'question': 'What is your name'}

response = requests.get(url, json=data)
result = response.json()['answer']
imagecontent = response.json()['image']
print(f'The result is: {result}')

img = base64.b64decode(imagecontent)
#img.save('test_recv/tmp.png')
with open('test_recv/tmp.png', 'wb') as f:
    f.write(img)