import os
import re
import logging
import nest_asyncio
import asyncio
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Apply nest_asyncio for compatibility
nest_asyncio.apply()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Quote for /start command
QUOTE = "“Work hard in silence, let your success make the noise.” 🚀"

# Pattern to detect links/usernames
PATTERN = re.compile(
    r'(@\w+|https?://\S+|t\.me/\S+|facebook\.com/\S+|instagram\.com/\S+|youtube\.com/\S+|whatsapp\.com/\S+|www\.\S+|bit\.ly)',
    re.IGNORECASE
)

# Flask app for health check
web_app = Flask(__name__)

@web_app.route("/")
def health_check():
    return "Bot is alive!", 200

def run_web_server():
    web_app.run(host="0.0.0.0", port=8000)

# Telegram: /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(QUOTE)

# Telegram: Delete messages with links
async def delete_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message.chat.type in ['group', 'supergroup'] and PATTERN.search(message.text or ""):
        try:
            await message.delete()
            logger.info(f"Deleted message in chat '{message.chat.title}'")
        except Exception as e:
            logger.warning(f"Failed to delete message in chat '{message.chat.id}': {e}")

# Telegram: Bot logic
async def main():
    TOKEN = os.getenv("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("BOT_TOKEN environment variable not set.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), delete_links))

    logger.info("Bot is running...")
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    # Start Flask web server in background for Koyeb health check
    threading.Thread(target=run_web_server).start()

    # Run the bot without closing the event loop (fixes RuntimeError)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
