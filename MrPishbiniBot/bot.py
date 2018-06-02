from telegram import Update, Message
from telegram.bot import Bot

WELCOME_MSG = ''
START_COMMAND = '/start'


class MrPishbiniBot:
    @staticmethod
    def update(bot: Bot, update: Update):
        Message.text
        if update.message:
            if update.message.text == START_COMMAND:
                MrPishbiniBot.start(bot, update)

    @staticmethod
    def start(bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, "hello")
