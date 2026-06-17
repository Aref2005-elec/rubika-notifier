import os
import time
import base64
import requests
from rubpy import Client, filters
from rubpy.types import Update

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SESSION_DATA = os.environ.get("SESSION_DATA")
SESSION_PATH = "/app/rubika_session"


def send_telegram(text):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        })
    except Exception as e:
        print(f"Telegram error: {e}")


def load_session():
    if SESSION_DATA:
        session_bytes = base64.b64decode(SESSION_DATA)
        with open(f"{SESSION_PATH}.rp", "wb") as f:
            f.write(session_bytes)
        print(f"Session saved to {SESSION_PATH}.rp")
    else:
        print("No SESSION_DATA found!")
        exit(1)


load_session()

while True:
    try:
        print("Starting Rubika listener...")
        bot = Client(name=SESSION_PATH)

        @bot.on_message_updates(filters.private)
        def on_private_message(update: Update):
            try:
                sender = getattr(update, 'author_title', None) or "ناشناس"
                text = getattr(update, 'text', None) or "[پیام بدون متن]"
                notify = (
                    f"📩 <b>پیام جدید در روبیکا</b>\n\n"
                    f"👤 <b>از:</b> {sender}\n"
                    f"💬 <b>پیام:</b> {text}"
                )
                send_telegram(notify)
                print(f"New message from {sender}: {text}")
            except Exception as e:
                print(f"Error processing message: {e}")

        send_telegram("✅ ربات وصل شد.")
        bot.run()

    except Exception as e:
        print(f"Connection lost: {e}")
        print("Reconnecting in 5 seconds...")
        time.sleep(5)
