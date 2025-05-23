import os
import re
import subprocess
from flask import Flask, request
import telegram
from telegram.ext import Dispatcher, MessageHandler, Filters, CallbackContext

# ملاحظة: في بيئة الإنتاج استخدم os.environ.get("BOT_TOKEN") بدلاً من كتابة التوكن مباشرة
TOKEN = "7690572227:AAHfLU9xMEeBVaBWCdwCJLlbVjML7zeXoms"

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

# Dispatcher ثابت
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, lambda update, context: handle_message(update, context)))

def is_email(text):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", text)

def is_phone(text):
    return re.match(r"^\+?\d{7,15}$", text)

def run_command(command_list, cwd=None):
    try:
        result = subprocess.run(command_list, capture_output=True, text=True, timeout=60, cwd=cwd)
        return result.stdout[-4000:] if result.stdout else "لا توجد نتائج."
    except Exception as e:
        return f"حدث خطأ أثناء التنفيذ: {str(e)}"

def run_sherlock(name):
    return run_command(["python3", "sherlock/sherlock.py", name, "--print-found"], cwd="sherlock")

def run_phoneinfoga(phone):
    return run_command(["python3", "phoneinfoga/phoneinfoga.py", "scan", "-n", phone], cwd="phoneinfoga")

def run_theharvester(email):
    return run_command([
        "python3", "theHarvester/theHarvester.py",
        "-d", email.split("@")[-1], "-b", "google,bing,duckduckgo"
    ], cwd="theHarvester")

def handle_message(update, context: CallbackContext):
    try:
        text = update.message.text.strip()
        chat_id = update.message.chat_id

        if is_email(text):
            result = run_theharvester(text)
        elif is_phone(text):
            result = run_phoneinfoga(text)
        else:
            result = run_sherlock(text)

        context.bot.send_message(chat_id=chat_id, text=result or "لم يتم العثور على نتائج.")
    except Exception as e:
        print(f"خطأ في handle_message: {str(e)}")

@app.route("/", methods=["GET"])
def index():
    return "البوت شغال بنجاح!"

@app.route("/", methods=["POST"])
def webhook():
    try:
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    except Exception as e:
        print(f"خطأ في webhook: {str(e)}")
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)