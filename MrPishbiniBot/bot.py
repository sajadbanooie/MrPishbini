from telegram import Update, Message
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram.bot import Bot

WELCOME_MSG = 'سلام خوش اومدین'
RULES_MSG = 'قوانین'

START_COMMAND = '/start'
RULES_COMMAND = 'قوانین'
MATCH_LIST_COMMAND = 'لیست بازی ها'
PISHBINI_COMMAND = 'ثبت پیشبینی'


class MrPishbiniBot:
    @staticmethod
    def update(bot: Bot, update: Update):
        if update.message:
            print(update.message)
            if update.message.text == START_COMMAND:
                MrPishbiniBot.start(bot, update)
            elif update.message.text == RULES_COMMAND:
                bot.send_message(update.message.chat_id,RULES_MSG)
            elif update.message.text == MATCH_LIST_COMMAND:
                MrPishbiniBot.match_list(bot, update)

    @staticmethod
    def start(bot: Bot, update: Update):
        bot.send_message(update.message.chat_id, WELCOME_MSG
                         , reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(RULES_COMMAND), KeyboardButton(MATCH_LIST_COMMAND),
                  KeyboardButton(PISHBINI_COMMAND)]]))

    @staticmethod
    def match_list(bot: Bot, update: Update):
        pass
