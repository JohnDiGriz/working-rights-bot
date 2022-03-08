import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ["TOKEN"]


def start(update, context):
    update.message.reply_text("""Відправте свою скаргу
Отправьте свою жалобу""")


def help(update, context):
    update.message.reply_text("""Використайте команду /compaint щоб відправити скаргу
Используйте комманду /complaint чтоб отправить жалобу""")


def receive_complaint(update, context):
    update.message.reply_text("""Ваша скарга прийнята
Ваша жалоба принята""")
    update.message.forward(chat_id=-1001773404147)
    context.bot.send_message(chat_id=-1001773404147, text="@"+update.message.from_user.username)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("complaint", start))
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(MessageHandler(Filters.text, receive_complaint))

    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://working-rights-bot.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
