import os
from flask import Flask, request
import telebot

API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك في بوت OSINT. أرسل اسم أو رقم أو إيميل للبحث.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.reply_to(message, "جاري البحث عن: " + message.text)
    # مكان استدعاء أدوات OSINT لاحقًا

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def index():
    return "Bot is running..."

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL"))
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
