import os
import re
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

QUOTE = "“Work hard in silence, let your success make the noise.” 🚀"
PATTERN = re.compile(r'(@\w+|https?://\S+)', re.IGNORECASE)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(QUOTE)

async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type in ['group', 'supergroup'] and PATTERN.search(message.text or ""):
        try:
            await message.delete()
            logger.info(f"Deleted message in {message.chat.title}")
        except Exception as e:
            logger.warning(f"Failed to delete message: {e}")

async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

    logger.info("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
