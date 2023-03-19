import os
import telebot
import requests
import io
import base64

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
    url = 'http://localhost:5000/api/chat/'
    # url = 'http://leekahwai.pythonanywhere.com:5566/api/chat/'
    # url = 'https://chatbot-endpoint.vercel.app/api/chat'
    data = {'question': message.text}
    response = requests.get(url, params=data)
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
