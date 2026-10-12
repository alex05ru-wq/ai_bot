import os
import telebot
from dotenv import load_dotenv
from gigachat import GigaChat

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GIGACHAT_KEY = os.getenv('GIGACHAT_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Подключаемся к GigaChat
giga = GigaChat(
    credentials=GIGACHAT_KEY,
    scope='GIGACHAT_API_PERS',  # для физлиц
    model='GigaChat-2',
    verify_ssl_certs=False       # чтобы не было проблем с сертификатами
)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я ИИ-бот на базе GigaChat. Напиши мне что-нибудь — я отвечу.'
    )


@bot.message_handler(content_types=['text'])
def chat(message):
    # Показываем, что бот "думает"
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        # Отправляем сообщение в GigaChat
        response = giga.chat(message.text)
        answer = response.choices[0].message.content

        bot.send_message(message.chat.id, answer)

    except Exception as e:
        print('Ошибка:', e)
        bot.send_message(
            message.chat.id,
            'Извини, не могу ответить. Попробуй ещё раз позже.'
        )


print('ИИ-бот запущен...')
bot.polling(none_stop=True)