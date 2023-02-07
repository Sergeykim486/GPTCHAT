import telebot
import openai

# insert your OpenAI API key here
openai.api_key = "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"

# insert your Telegram bot API key here
API_KEY = "6130814802:AAGll0wArHRABMzTMmHM4sv2ZMqVSQV6GXU"
bot = telebot.TeleBot(API_KEY)


@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Привет, Я Telegram bot для работы в чат GPT3.")


def split_response(response):
    # maximum number of characters per message
    max_chars = 4096
    if len(response) > max_chars:
        return [response[i : i + max_chars] for i in range(0, len(response), max_chars)]
    else:
        return [response]


@bot.message_handler(func=lambda message: True)
def chat_with_gpt3(message):
    response = (
        openai.Completion.create(
            engine="text-davinci-002",
            prompt="You: " + message.text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        .choices[0]
        .text
    )
    for chunk in split_response(response):
        bot.reply_to(message, "Нейросеть: " + chunk)


bot.polling()
