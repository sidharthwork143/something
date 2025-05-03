import os
import re
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Telegram token from environment
TOKEN = os.getenv("BOT_TOKEN")

# Flask app for webhook (for Koyeb)
app = Flask(__name__)
bot_app = None  # Will be set after Telegram app initializes

# Regex patterns for usernames and telegram links
USERNAME_PATTERN = re.compile(r'@\w+')
LINK_PATTERN = re.compile(r'(https?://)?(www\.)?(t\.me|telegram\.me)/\w+')

# Message handler
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        if USERNAME_PATTERN.search(text) or LINK_PATTERN.search(text):
            try:
                await context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
                print("Deleted a message containing username or link.")
            except Exception as e:
                print(f"Error deleting message: {e}")

# Flask route for webhook
@app.route("/", methods=["POST"])
def webhook():
    if bot_app:
        update = Update.de_json(request.get_json(force=True), bot_app.bot)
        bot_app.update_queue.put_nowait(update)
    return "OK"

# Telegram bot initialization
async def main():
    global bot_app
    bot_app = ApplicationBuilder().token(TOKEN).build()

    # Only handle text messages in groups
    bot_app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, filter_messages))

    # Set webhook (replace YOUR_DOMAIN with your Koyeb app domain)
    webhook_url = os.getenv("WEBHOOK_URL")
    await bot_app.bot.set_webhook(url=webhook_url)

    # Start Flask app
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Start everything
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
