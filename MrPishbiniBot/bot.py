from telegram import Update, Message
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram.bot import Bot

WELCOME_MSG = 'سلام خوش اومدین'
START_COMMAND = '/start'
RULES_COMMAND = ''
MATCH_LIST_COMMAND = ''
PISHBINI_COMMAND = ''


class MrPishbiniBot:
    @staticmethod
    def update(bot: Bot, update: Update):
        if update.message:
            print(update.message)
            if update.message.text == START_COMMAND:
                MrPishbiniBot.start(bot, update)

    @staticmethod
    def start(bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, WELCOME_MSG
                         , reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(RULES_COMMAND), KeyboardButton(MATCH_LIST_COMMAND),
                  KeyboardButton(PISHBINI_COMMAND)]]))
