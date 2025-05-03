
import os
import re
from telegram import Update, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Bot token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Regex to detect @username or Telegram link
USERNAME_PATTERN = re.compile(r'@\w+')
LINK_PATTERN = re.compile(r'(https?://)?(www\.)?(t\.me|telegram\.me)/\w+')

# 📸 Motivational photo and quote
PHOTO_PATH = "welcome.jpg"  # Make sure this file exists in your directory
QUOTE = "✨ *Welcome!* ✨\n\n_“The journey of a thousand miles begins with a single step.”_"

# Handle /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        with open(PHOTO_PATH, 'rb') as photo:
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=QUOTE,
                parse_mode='Markdown'
            )
    except Exception as e:
        print(f"Error sending start message: {e}")

# Filter messages in group
async def filter_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        text = update.message.text
        if USERNAME_PATTERN.search(text) or LINK_PATTERN.search(text):
            try:
                await context.bot.delete_message(
                    chat_id=update.message.chat_id,
                    message_id=update.message.message_id
                )
                print("🚫 Message deleted!")
            except Exception as e:
                print(f"Error deleting message: {e}")

# Main function
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & filters.ChatType.GROUPS, filter_messages))

    print("✅ Bot is running (Polling mode)...")
    await app.run_polling()

# Entry point
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
