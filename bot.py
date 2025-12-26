import os
import json
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("7862802172:AAFJ4tJ4aIBEDZ-jrW1yptvhEC-uyPhyx5U")

def is_paid(user_id):
    if not os.path.exists("users.json"):
        return False

    with open("users.json", "r") as f:
        users = json.load(f)

    if str(user_id) in users:
        expiry = datetime.strptime(users[str(user_id)], "%Y-%m-%d")
        return datetime.now() <= expiry

    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "यह bot सिर्फ PAID users के लिए है।\n"
        "Admin से संपर्क करें।"
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not is_paid(user_id):
        await update.message.reply_text("❌ Access denied. Paid user नहीं है।")
        return

    if update.message.document:
        await update.message.reply_text("✅ File received (paid user).")


async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    await app.run_polling(close_loop=False)


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
