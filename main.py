import os
from dotenv import load_dotenv
import telebot
import requests

load_dotenv()
token = os.environ["TOKEN"]
bot = telebot.TeleBot(token)


def format_message(poem):
    poem_author = poem["author"]
    poem_title = poem["title"]
    poem_text = "\n"
    for line in poem["lines"]:
        poem_text += f"{line}\n"
    return f'Poem <b>"{poem_title}"</b> by <b>{poem_author}</b>\n{poem_text}'


def fetch_poem(poet=""):
    if poet:
        url = f"https://poetrydb.org/author/{poet}/title,author,lines"
    else:
        url = "https://poetrydb.org/random/1/title,author,lines"

    return requests.get(url).json()[0]


def send_poem(message, poem_message):
    error_message = "Something went wrong, please try again ❗️"
    try:
        bot.send_message(message.chat.id, poem_message, parse_mode="html")
    except BaseException:
        bot.send_message(message.chat.id, error_message, parse_mode="html")


@bot.message_handler(commands=["random"])
def get_random_poem(message):
    random_poem = fetch_poem()
    poem_message = format_message(random_poem)
    send_poem(message, poem_message)


@bot.message_handler(commands=["author"])
def get_poem_by_author(message):
    input_author = " ".join(message.text.split()[1:]).title()
    random_poem = fetch_poem(poet=input_author)
    poem_message = format_message(random_poem)
    send_poem(message, poem_message)


bot.polling(none_stop=True)
