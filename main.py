import json
import time
import telegram
from telegram.ext import Updater, CommandHandler

def start(update, context):
    user_id = update.message.from_user.id
    if not user_exists(user_id):
        register_user(user_id)
    update.message.reply_text("Hi! How can I help you today?")

def check_request_limit(user_id):
    user_data = get_user_data(user_id)
    if user_data["request_count"] >= 10:
        return False
    user_data["request_count"] += 1
    save_user_data(user_id, user_data)
    return True

def chat(update, context):
    user_id = update.message.from_user.id
    if check_request_limit(user_id):
        response = "You've already made 10 requests today. Try again tomorrow."
    else:
        response = "This is a response from the ChatGPT model."
    update.message.reply_text(response)

def register_user(user_id):
    user_data = {
        "user_id": user_id,
        "request_count": 0,
        "timestamp": int(time.time())
    }
    save_user_data(user_id, user_data)

def get_user_data(user_id):
    with open("users.json", "r") as file:
        data = json.load(file)
    return data.get(str(user_id), {})

def save_user_data(user_id, user_data):
    with open("users.json", "r") as file:
        data = json.load(file)
    data[str(user_id)] = user_data
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)

def user_exists(user_id):
    with open("users.json", "r") as file:
        data = json.load(file)
    return str(user_id) in data

if __name__ == "__main__":
    with open("users.json", "w") as file:
        json.dump({}, file)

    updater = Updater(token="6130814802:AAGll0wArHRABMzTMmHM4sv2ZMqVSQV6GXU", use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    chat_handler = CommandHandler("chat", chat)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(chat_handler)
    updater.start_polling()
