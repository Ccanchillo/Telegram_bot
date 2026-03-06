import os
from flask import Flask, request
import telebot

# Configuración
TOKEN = os.getenv('TOKEN') # Lo configuraremos en la nube después
URL = os.getenv('URL_APP') # La URL que nos dará Render
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('uft-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([Update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL + TOKEN)
    return "Bot funcionando correctamente", 200

# Lóica del Bot: Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.repley_to(message, "¡Hola! Soy tu bot funcional en Python. ¿En qué puedo ayudarte?")

# Respuesta a mensajes de texto
@bot.message_handler(func=lambda message:True)
def echo_all(message):
    bot.reply_to(message, f"Me dijiste: {message.text}")

if __name__ == "__name__":
    appp.run(host="0.0.0.0", port=int(os.environ.get('PORT, 5000')))