import logging
import re
import os
from telegram import Update, ChatMember
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters,
)

# Logging for debugging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ✨ Start command message
START_QUOTE = "“Work hard in silence, let your success make the noise.” 🚀"

# Username and link pattern
USERNAME_OR_LINK = re.compile(r'(@\w+|https?://\S+)', re.IGNORECASE)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_QUOTE)

# Message monitor and delete
async def filter_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message and message.chat.type in ['group', 'supergroup']:
        text = message.text or ""
        if USERNAME_OR_LINK.search(text):
            try:
                await message.delete()
                logger.info(f"Deleted message in {message.chat.title}: {text}")
            except Exception as e:
                logger.warning(f"Failed to delete message: {e}")

# Main function to run bot
async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), filter_message))

    logger.info("Bot started...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
