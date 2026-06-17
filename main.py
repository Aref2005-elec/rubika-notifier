import asyncio
import os
import requests
from rubpy import Client, filters
from rubpy.types import Update

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
SESSION_NAME = os.environ.get("SESSION_NAME", "rubika_session")


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


async def main():
    print("Starting Rubika listener...")

    bot = Client(name=SESSION_NAME)

    @bot.on_message_updates(filters.private)
    async def on_private_message(update: Update):
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
            print(f"Error: {e}")

    send_telegram("✅ ربات روشن شد و در حال نظارت روبیکاست.")
    bot.run()


if __name__ == "__main__":
    asyncio.run(main())
