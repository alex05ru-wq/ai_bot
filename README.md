# Telegram-бот с GigaChat AI

Telegram-бот на Python, который отвечает на любые сообщения с помощью нейросети GigaChat от Сбера.

## Возможности

- Команда /start — приветствие
- Ответ на любое текстовое сообщение через GigaChat
- Осмысленные ответы: факты, объяснения, анекдоты, помощь с кодом и текстом
- Индикатор «печатает…» во время генерации ответа
- Память диалога: бот помнит последние 10 сообщений каждого пользователя
- Команда /reset — начать разговор заново
- Длинные ответы автоматически делятся на несколько сообщений (лимит Telegram 4096 символов)

## Технологии

- Python 3
- pyTelegramBotAPI — работа с Telegram Bot API
- GigaChat — официальная библиотека для GigaChat API
- python-dotenv — загрузка ключей из .env

## Установка и запуск

1. Клонируй репозиторий:
```bash
git clone https://github.com/alex05ru-wq/ai_bot.git
cd ai_bot
```
2. Установи зависимости:
```bash
pip install -r requirements.txt
```
3. Создай бота в Telegram через @BotFather и получи токен.

4. Получи ключ GigaChat API на Sber Studio (developers.sber.ru).

5. Создай файл .env в корне проекта:
```bash
TELEGRAM_TOKEN=твой_токен_от_BotFather
GIGACHAT_KEY=твой_ключ_из_Sber_Studio
GIGACHAT_CA_BUNDLE=russian_trusted_root_ca.cer
```
Строка GIGACHAT_CA_BUNDLE необязательна: это путь к сертификату Минцифры для защищённого соединения с GigaChat. Без неё бот работает, но проверка SSL отключена.
6. Запусти бота:
```bash
python bot.py
```
7. Открой бота в Telegram и напиши /start.

## Структура проекта

ai_bot/
├── bot.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md

## Как это работает

1. Пользователь пишет сообщение боту в Telegram.
2. Бот передаёт в GigaChat API текст вместе с историей последних сообщений, поэтому понимает уточняющие вопросы.
3. GigaChat генерирует ответ с помощью нейросети.
4. Бот отправляет ответ пользователю.

## Автор

Alex — https://github.com/alex05ru-wq



