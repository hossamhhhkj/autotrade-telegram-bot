import os
import telebot
from flask import Flask, request

# اقرأ توكن البوت من متغير بيئة
TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = os.environ.get("GROUP_ID")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@app.route(f'/{TOKEN}', methods=['POST'])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return 'OK', 200

# لما البوت يبدأ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "🤖 البوت شغال تمام يا حسام!")

# مثال بسيط لرد تلقائي
@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if "يلا بينا" in message.text:
        bot.send_message(GROUP_ID, "🚀 جاري البحث عن أفضل صفقة...")
    else:
        bot.send_message(message.chat.id, "📍 تم استلام رسالتك.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
