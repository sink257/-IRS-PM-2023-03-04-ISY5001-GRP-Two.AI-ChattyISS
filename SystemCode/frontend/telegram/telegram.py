import os
import telebot
import requests
import io
import base64
import json
import urllib.parse

# This is your bot's API token
# ChattyISS_bot
BOT_TOKEN = '6065015392:AAGSkWEXlLLdxPxMPfPTh5lwZj2ll9YkuO8'

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to ChattyISS, the ISS Chatbot based on transformer technology")

@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    # Does a connection check to ChattyISS coreback end
    #url = 'http://localhost:5000/api/chat/'
    #data = {'question': message.text} 
    #encoded_params = json.dumps({'data': data})
    #response = requests.get(url, params=encoded_params, headers={'Content-Type': 'application/json'})
    #if response.status_code == 200:
    url = 'http://localhost:5000/api/chat/'
    data = {'question': message.text}
    encoded_params = urllib.parse.urlencode({'data': json.dumps(data)})
    response = requests.get(url + '?' + encoded_params)
    if response.status_code == 200:
        result = response.json()['answer']
        print (result)
        message2 = message
        bot.reply_to(message, result)
        imagecontent = response.json()['image']
        img = base64.b64decode(imagecontent)
        with open('test_recv/tmp.png', 'wb') as f:
            f.write(img)
        myfile = open('test_recv/tmp.png', 'rb')

        input_file = telebot.types.InputFile(myfile)
        bot.send_document(message2.chat.id, input_file)
    else:
        bot.reply_to(message,"The connection to ChattyISS core engine is down. Try again later")

bot.infinity_polling()
