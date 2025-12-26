import os
import json
from datetime import datetime

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================
BOT_TOKEN = os.getenv("BOT_TOKEN")

USERS_FILE = "users.json"
DATE_FORMAT = "%Y-%m-%d"
# ==========================================


def is_paid(user_id: int) -> bool:
    if not os.path.exists(USERS_FILE):
        return False

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    user_id = str(user_id)
    if user_id not in users:
        return False

    try:
        expiry = datetime.strptime(users[user_id], DATE_FORMAT)
        return datetime.now() <= expiry
    except Exception:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "यह bot सिर्फ PAID users के लिए है.\n"
        "Admin से संपर्क करें."
    )


async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not is_paid(user_id):
        await update.message.reply_text("❌ Access denied.\nPaid user नहीं हो.")
        return

    if update.message.document:
        await update.message.reply_text("✅ File received (paid user).")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("🤖 Bot started...")
    await app.run_polling()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
