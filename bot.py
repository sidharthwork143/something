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

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Message deletion pattern
PATTERN = re.compile(r'(@\w+|https?://\S+)', re.IGNORECASE)
QUOTE = "“Work hard in silence, let your success make the noise.” 🚀"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(QUOTE)

# Auto-delete links and usernames
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type in ['group', 'supergroup'] and PATTERN.search(message.text or ""):
        try:
            await message.delete()
            logger.info(f"Deleted a message in {message.chat.title}")
        except Exception as e:
            logger.warning(f"Failed to delete message: {e}")

# Bot main logic
async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

    logger.info("Bot is running...")
    await app.run_polling()

# Async-safe launch for Koyeb & local
if __name__ == "__main__":
    import asyncio

    try:
        asyncio.get_event_loop().run_until_complete(main())
    except RuntimeError:
        import nest_asyncio
        nest_asyncio.apply()
        asyncio.get_event_loop().run_until_complete(main())
