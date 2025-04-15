import os
import re
import subprocess
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, filters, CallbackContext

# جلب التوكن من البيئة
TOKEN = os.environ.get("BOT_TOKEN")
bot = Bot(token=TOKEN)

# إعداد Flask
app = Flask(__name__)

# التحقق من أنواع الإدخال
def is_email(text):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", text)

def is_phone(text):
    return re.match(r"^\+?\d{7,15}$", text)

# تشغيل الأدوات
def run_command(command_list, cwd=None):
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, timeout=60, cwd=cwd)
        return result.stdout[-4000:] if result.stdout else "لا توجد نتائج."
    except Exception as e:
        return f"حدث خطأ: {str(e)}"

def run_sherlock(name):
    return run_command(["python3", "sherlock/sherlock.py", name, "--print-found"], cwd="sherlock")

def run_phoneinfoga(phone):
    return run_command(["python3", "phoneinfoga/phoneinfoga.py", "scan", "-n", phone], cwd="phoneinfoga")

def run_theharvester(email):
    return run_command([
        "python3", "theHarvester/theHarvester.py",
        "-d", email.split("@")[-1], "-b", "google,bing,duckduckgo"
    ], cwd="theHarvester")

# المعالجة الرئيسية للرسائل
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.strip()
    chat_id = update.effective_chat.id

    if is_email(text):
        result = run_theharvester(text)
    elif is_phone(text):
        result = run_phoneinfoga(text)
    else:
        result = run_sherlock(text)

    context.bot.send_message(chat_id=chat_id, text=result or "لم يتم العثور على نتائج.")

# المسار الرئيسي لعرض أن البوت يعمل
@app.route("/", methods=["GET"])
def index():
    return "Bot is running!"

# webhook الخاص بـ Telegram
@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    dispatcher.process_update(update)
    return "OK"

# التشغيل المحلي (لن يعمل على Render)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)