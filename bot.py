from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import zipfile, json, os
from datetime import datetime

BOT_TOKEN = os.getenv("BOT_TOKEN")

def is_paid(user_id):
    with open("users.json", "r") as f:
        users = json.load(f)
    if str(user_id) in users:
        expiry = datetime.strptime(users[str(user_id)], "%Y-%m-%d")
        return datetime.now() <= expiry
    return False

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if not is_paid(user_id):
        await update.message.reply_text("❌ Paid users only.\nContact Admin 💰")
        return

    doc = update.message.document
    file = await doc.get_file()
    await file.download_to_drive("file.zip")

    with zipfile.ZipFile("file.zip", 'r') as zip_ref:
        zip_ref.extractall("extracted")

    await update.message.reply_text("✅ File extracted successfully")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
app.run_polling()
