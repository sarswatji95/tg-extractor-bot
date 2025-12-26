import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "यह bot केवल PAID users के लिए है।\n"
        "Admin से संपर्क करें।"
    )

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ File received.")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
