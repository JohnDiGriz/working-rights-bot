import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os

PORT = int(os.environ.get('PORT', 5000))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = os.environ["TOKEN"]
CHAT = os.environ["CHAT"]


def start(update, context):
    keyboard = [["Працедавець відмовляється платити заробітну плату, мотивуючи це війною"],
                ["Працедавець примусово відправляє у неоплачувану відпустку або намагається звільнити"],
                ["Працедавець відмовляється виплачувати понаднормові/нічні/будь-які інші види доплат"],
                ["Я залишися_ась без роботи через війну. Яку допомогу від держави я можу отримати?"],
                ["Я мобілізувався_ась / пішов_ла добровольцем у Територіальну Оборону (ТрО)"],
                ["Я евакуювався_лась / втратив_ла зв'язок із працедавцем / не можу потрапити на робоче місце через бойові дії"],
                ["Якої позиції дотримуватися на переговорах з працедавцем?"]]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text("""Привіт!

Цей бот створили активісти ГО "Соціальний рух", щоб консультувати вас на рахунок порушення трудових прав.

Будь ласка, напишіть своє звернення, або виберіть одну з опцій
Ми відповімо вам у найближчий час.""", reply_markup = reply_markup)
    



def receive_complaint(update, context):
    update.message.reply_text("""Ваше звернення прийняте""")
    update.message.forward(chat_id=CHAT)
    context.bot.send_message(chat_id=CHAT, text="@"+update.message.from_user.username)


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(MessageHandler(Filters.text, receive_complaint))

    dp.add_error_handler(error)

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://working-rights-bot.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
