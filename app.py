import os
from telegram.ext import Updater, CommandHandler
from rag_utils import answer_query

# Read token from environment variable for safety
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "ADD_YOUR_TELEGRAM_BOT_TOKEN_HERE")

def start(update, context):
    msg = (
        "👋 Hi! I'm a Mini-RAG Telegram Bot.\n\n"
        "Use /ask <your question> to query the knowledge base.\n"
        "Example:\n"
        "/ask What is data science?"
    )
    update.message.reply_text(msg)

def help_command(update, context):
    msg = (
        "📖 Help - Mini-RAG Bot\n\n"
        "/ask <query>  - Ask a question based on stored documents\n"
        "/start        - Introduction message\n"
        "/help         - Show this help message\n\n"
        "Make sure the backend RAG pipeline is built using build_db.py."
    )
    update.message.reply_text(msg)

def ask(update, context):
    query = " ".join(context.args)
    if not query:
        update.message.reply_text("❗ Please use: /ask <your question>")
        return
    try:
        answer = answer_query(query)
        update.message.reply_text(answer)
    except Exception as e:
        update.message.reply_text(f"⚠ Error while answering: {e}")

def main():
    if TOKEN.startswith("ADD_YOUR_TELEGRAM_BOT_TOKEN"):
        print("⚠ Please set TELEGRAM_BOT_TOKEN environment variable or edit app.py.")
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("ask", ask))

    print("🤖 Telegram Mini-RAG Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
