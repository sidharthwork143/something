import os
import re
import logging
import nest_asyncio
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Allow asyncio to work inside certain environments (e.g., Koyeb or Jupyter)
nest_asyncio.apply()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quote to send on /start
QUOTE = "“Work hard in silence, let your success make the noise.” 🚀"

# Pattern to detect links, usernames, and common platforms
PATTERN = re.compile(
    r'(@\w+|https?://\S+|t\.me/\S+|facebook\.com/\S+|instagram\.com/\S+|youtube\.com/\S+|whatsapp\.com/\S+|www\.\S+)',
    re.IGNORECASE
)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(QUOTE)

# Detect and delete link messages in group chats
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type in ['group', 'supergroup'] and PATTERN.search(message.text or ""):
        try:
            await message.delete()
            logger.info(f"Deleted message in chat '{message.chat.title}'")
        except Exception as e:
            logger.warning(f"Failed to delete message in chat '{message.chat.id}': {e}")

# Main function to start the bot
async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set. Please configure it on Koyeb.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

    logger.info("Bot is running...")
    await app.run_polling()

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())

