import os
from collections import defaultdict

import telebot
from dotenv import load_dotenv
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GIGACHAT_KEY = os.getenv('GIGACHAT_KEY')
# Путь к сертификату Минцифры (необязательно, см. README)
CA_BUNDLE = os.getenv('GIGACHAT_CA_BUNDLE')

SYSTEM_PROMPT = 'Ты дружелюбный помощник в Telegram. Отвечай понятно и по делу.'
MAX_HISTORY = 10        # сколько последних сообщений помнить
TG_LIMIT = 4096         # максимальная длина сообщения в Telegram

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Если сертификат указан — проверяем SSL как положено, иначе отключаем проверку
if CA_BUNDLE:
    giga = GigaChat(credentials=GIGACHAT_KEY, scope='GIGACHAT_API_PERS',
                    model='GigaChat-2', ca_bundle_file=CA_BUNDLE)
else:
    giga = GigaChat(credentials=GIGACHAT_KEY, scope='GIGACHAT_API_PERS',
                    model='GigaChat-2', verify_ssl_certs=False)

# История диалога для каждого пользователя: {chat_id: [Messages, ...]}
history = defaultdict(list)


def split_text(text, limit=TG_LIMIT):
    """Режет длинный текст на части, стараясь резать по переносам строк."""
    parts = []
    while len(text) > limit:
        cut = text.rfind('\n', 0, limit)
        if cut <= 0:          # переноса нет — режем по пробелу
            cut = text.rfind(' ', 0, limit)
        if cut <= 0:          # и пробела нет — режем жёстко
            cut = limit
        parts.append(text[:cut])
        text = text[cut:].lstrip()
    if text:
        parts.append(text)
    return parts


@bot.message_handler(commands=['start'])
def start(message):
    history.pop(message.chat.id, None)
    bot.send_message(
        message.chat.id,
        'Привет! Я ИИ-бот на базе GigaChat. Напиши мне что-нибудь — я отвечу.\n\n'
        'Я помню наш разговор. Начать заново: /reset'
    )


@bot.message_handler(commands=['reset'])
def reset(message):
    history.pop(message.chat.id, None)
    bot.send_message(message.chat.id, 'Начинаем разговор с чистого листа.')


@bot.message_handler(content_types=['text'])
def chat(message):
    bot.send_chat_action(message.chat.id, 'typing')

    user_history = history[message.chat.id]
    user_history.append(Messages(role=MessagesRole.USER, content=message.text))

    try:
        # Отправляем системную подсказку + последние сообщения диалога
        payload = Chat(messages=[Messages(role=MessagesRole.SYSTEM, content=SYSTEM_PROMPT)]
                       + user_history[-MAX_HISTORY:])
        response = giga.chat(payload)
        answer = response.choices[0].message.content
    except Exception as e:
        print('Ошибка GigaChat:', e)
        user_history.pop()  # убираем вопрос, на который не ответили
        bot.send_message(message.chat.id, 'Извини, не могу ответить. Попробуй ещё раз позже.')
        return

    user_history.append(Messages(role=MessagesRole.ASSISTANT, content=answer))
    # Храним только последние сообщения, чтобы память не росла бесконечно
    history[message.chat.id] = user_history[-MAX_HISTORY:]

    for part in split_text(answer):
        bot.send_message(message.chat.id, part)


print('ИИ-бот запущен...')
bot.infinity_polling()
