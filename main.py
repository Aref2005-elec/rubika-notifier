import asyncio
import os
import rubika
import requests

RUBIKA_PHONE = os.environ.get("RUBIKA_PHONE")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "HTML"})


async def main():
    print("Starting Rubika listener...")
    send_telegram("✅ ربات روشن شد و در حال نظارت روبیکاست.")

    async with rubika.Client(RUBIKA_PHONE) as client:

        @client.on(rubika.handlers.MessageUpdates())
        async def on_message(message):
            try:
                sender_name = message.author_object.first_name or "ناشناس"
                last_name = message.author_object.last_name or ""
                full_name = f"{sender_name} {last_name}".strip()
                text = message.text or "[پیام بدون متن]"

                notify = (
                    f"📩 <b>پیام جدید در روبیکا</b>\n\n"
                    f"👤 <b>از:</b> {full_name}\n"
                    f"💬 <b>پیام:</b> {text}"
                )
                send_telegram(notify)
                print(f"New message from {full_name}: {text}")
            except Exception as e:
                print(f"Error processing message: {e}")

        await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
