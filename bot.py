from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
import json
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")

def is_paid(user_id):
    if not os.path.exists("users.json"):
        return False
    with open("users.json", "r") as f:
        users = json.load(f)
    if str(user_id) in users:
        expiry = datetime.strptime(users[str(user_id)], "%Y-%m-%d")
        return datetime.now() <= expiry
    return False

def start(update, context):
    update.message.reply_text(
        "👋 Welcome!\n\n"
        "यह bot सिर्फ PAID users के लिए है.\n"
        "Admin से संपर्क करें."
    )

def handle_file(update, context):
    user_id = update.message.from_user.id

    if not is_paid(user_id):
        update.message.reply_text("❌ Access denied. Paid user नहीं हो.")
        return

    if update.message.document:
        update.message.reply_text("✅ File received (paid user).")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.document, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
