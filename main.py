from flask import Flask
from threading import Thread
import telebot
import requests
from bs4 import BeautifulSoup
import os

# تشغيل السيرفر الخلفي لـ Replit
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# إدخال التوكن من المتغيرات السرية
API_TOKEN = os.environ['API_TOKEN']
bot = telebot.TeleBot(API_TOKEN)

def search_emobiletracker(number):
    try:
        url = f"https://www.emobiletracker.com/track/?phone={number}&submit=Track"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.find("table", class_="tracking-table")
        if table:
            rows = table.find_all("tr")
            info = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) == 2:
                    key = cols[0].get_text(strip=True)
                    val = cols[1].get_text(strip=True)
                    info.append(f"{key}: {val}")
            return "\n".join(info)
        else:
            return "لا توجد بيانات واضحة من emobiletracker."
    except:
        return "حدث خطأ أثناء البحث في emobiletracker."

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if message.text.startswith("+") or message.text.isdigit():
        bot.send_message(message.chat.id, "جارٍ البحث عن الرقم من emobiletracker...")
        result = search_emobiletracker(message.text.strip())
        bot.send_message(message.chat.id, result)
    else:
        bot.send_message(message.chat.id, "أرسل رقمًا يبدأ بـ + أو بدون رموز.")

# بدء السيرفر وتشغيل البوت
keep_alive()
bot.infinity_polling()