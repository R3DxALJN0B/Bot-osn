
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

TOKEN = "7755841021:AAHGqB14m6OnJocFrvXcef6E8HwU1gOyYWU"

app = Flask(__name__)

bot_app = Application.builder().token(TOKEN).build()

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً! أرسل أي اسم للبحث عن معلومات.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"جاري البحث عن: {text}\n(هذه نسخة تجريبية)")

bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Webhook endpoint
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        bot_app.update_queue.put(update)
    return "ok"

# تشغيل الخادم
if __name__ == "__main__":
    bot_app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url="https://telegram-bot-9bnb.onrender.com/webhook"
    )
