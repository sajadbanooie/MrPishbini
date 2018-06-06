from telegram import Update, Message, Chat, ForceReply
from telegram import User as TelegramUser
from telegram.replykeyboardmarkup import ReplyKeyboardMarkup
from telegram import KeyboardButton
from telegram.utils.helpers import mention_markdown
from telegram.bot import Bot

from MrPishbiniBot.models import Match, User, Pishbini

from django.utils.timezone import get_current_timezone

import datetime

WELCOME_MSG = 'سلام خوش اومدین'
RULES_MSG = 'قوانین'

START_CMD = '/start'  # done
RULES_CMD = 'قوانین'  # done
MATCH_LIST_CMD = 'لیست بازی ها'  # done
PISHBINI_CMD = 'ثبت پیشبینی'
PRE_PISHBINI_CMD = 'ثبت پیشبینی'
MATCH_PISHBINI_CMD = 'ثبت پیشبینی بازی ها'
MY_PISHBINIS_CMD = 'پیشبینی های من'
SCORES_CMD = 'جدول امتیاز ها'
CANCEL_CMD = ''

STATUS_IDLE = 0
STATUS_PISHBINI_T1 = 1
STATUS_PISHBINI_T2 = 2
STATUS_PISHBINI_PT1 = 3
STATUS_PISHBINI_PT2 = 4
STATUS_PISHBINI_FINAL = 5
STATUS_PRE_PISHBINI = 6

BEGIN_TIME = ''

user_temp_data = dict()


class MrPishbiniBot:
    @staticmethod
    def update(bot: Bot, update: Update):
        if update.message:
            print(update.message)
            if update.message.text == START_CMD:
                MrPishbiniBot.start(bot, update)
            elif update.message.text == RULES_CMD:
                bot.send_message(update.message.chat_id, RULES_MSG)
            elif update.message.text == MATCH_LIST_CMD:
                MrPishbiniBot.match_list(bot, update)
            elif update.message.text == CANCEL_CMD:
                user_temp_data[update.message.from_user.id] = {'status': STATUS_IDLE, 'temp_data': None}
            elif update.message.text == PISHBINI_CMD:
                # TODO
                # if datetime.datetime.strptime(BEGIN_TIME, "") <= datetime.datetime.now(get_current_timezone()):
                #     MrPishbiniBot.pishbini(bot, update)
                #     return
                bot.send_message(update.message.chat_id, "از بین اینها انخاب کن"
                                 , reply_markup=ReplyKeyboardMarkup(
                        [[KeyboardButton(MATCH_PISHBINI_CMD), KeyboardButton(PRE_PISHBINI_CMD)]]))
            elif update.message.text == MATCH_PISHBINI_CMD:
                MrPishbiniBot.pishbini(bot, update)
            elif update.message.text == PRE_PISHBINI_CMD:
                MrPishbiniBot.pre_pishbini(bot, update)
            elif update.message.text == SCORES_CMD:
                MrPishbiniBot.scores(bot, update)
            elif update.message.text == MY_PISHBINIS_CMD:
                MrPishbiniBot.my_pishbinis(bot, update)

    @staticmethod
    def start(bot: Bot, update: Update):
        if update.message.chat.type != Chat.PRIVATE:
            bot.send_message(update.message.chat_id, "unsupported")
            return

        bot.send_message(update.message.chat_id, WELCOME_MSG
                         , reply_markup=ReplyKeyboardMarkup(
                [[KeyboardButton(RULES_CMD), KeyboardButton(MATCH_LIST_CMD),
                  KeyboardButton(PISHBINI_CMD)]]))

        user_temp_data[update.message.from_user.id] = {'status': STATUS_IDLE, 'temp_data': None}

        u, created = User.objects.get_or_create(first_name=update.message.from_user.first_name, id=update.message.from_user.id)
        if update.message.from_user.last_name:
            u.last_name = update.message.from_user.last_name
        if update.message.from_user.username:
            u.username = update.message.from_user.username
        u.save()

    @staticmethod
    def match_list(bot: Bot, update: Update):
        msg = ''
        i = 1
        for m in Match.objects.all():
            msg += '(' + str(i) + ') ' + m.teams.all()[0].flag + m.teams.all()[0].name + ' - ' \
                   + m.teams.all()[1].name + m.teams.all()[1].flag \
                   + '    ' + str(m.time) + '\n'
            i += 1

        if msg == '':
            msg = 'هیچی'

        bot.send_message(update.message.chat_id, msg)

    @staticmethod
    def scores(bot: Bot, update: Update):
        # TODO
        pass

    @staticmethod
    def my_pishbinis(bot: Bot, update: Update):
        # TODO
        pass

    @staticmethod
    def pishbini(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        if user_temp_data[tg_user.id]['status'] == STATUS_PISHBINI_T1:
            MrPishbiniBot.pishbini_t1(bot, update)
        if user_temp_data[tg_user.id]['status'] == STATUS_PISHBINI_T2:
            MrPishbiniBot.pishbini_t2(bot, update)
        if user_temp_data[tg_user.id]['status'] == STATUS_PISHBINI_PT1:
            MrPishbiniBot.pishbini_pt1(bot, update)
        if user_temp_data[tg_user.id]['status'] == STATUS_PISHBINI_PT2:
            MrPishbiniBot.pishbini_pt2(bot, update)
        if user_temp_data[tg_user.id]['status'] == STATUS_PISHBINI_FINAL:
            MrPishbiniBot.pishbini_final(bot, update)

        msg = ''
        i = 1
        for m in Match.objects.filter(
                time__gt=datetime.datetime.now(tz=get_current_timezone()) + datetime.timedelta(hours=24)):
            msg += '(' + str(i) + ') ' + m.teams.all()[0].flag + m.teams.all()[0].name + ' - ' \
                   + m.teams.all()[1].name + m.teams.all()[1].flag \
                   + '    ' + str(m.time) + '\n'
            i += 1

        if msg == '':
            bot.send_message(update.message.chat_id, "هیچ بازی ای جهت پیشبینی وجود ندارد")
            return

        bot.send_message(update.message.chat_id, msg)

        keyboard = []

        for j in range(i//3):
            keyboard.append([])
            for k in range(i % 3):
                keyboard[j].append(KeyboardButton(str(j*3 + k + 1)))

        keyboard[i // 3][i % 3] = KeyboardButton(CANCEL_CMD)

        bot.send_message(update.message.chat_id, "", reply_markup=ReplyKeyboardMarkup(keyboard))
        user_temp_data[tg_user.id]['status'] = STATUS_PISHBINI_T1

    @staticmethod
    def pishbini_t1(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        user = User.objects.get(id=update.message.from_user.id)
        match = Match.objects.filter(
            time__gt=datetime.datetime.now(tz=get_current_timezone()) + datetime.timedelta(hours=24))[
            int(update.message.text) - 1]
        user_temp_data[tg_user.id]['temp_data'] = Pishbini(user=user, match=match)

        bot.send_message(update.message.chat_id,
                         "به نظرت {} چند تا گل میزنه؟".format(match.teams.all()[0].name),
                         reply_markup=ForceReply())

        user_temp_data[tg_user.id]['status'] = STATUS_PISHBINI_T2

    @staticmethod
    def pishbini_t2(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        user_temp_data[tg_user.id]['temp_data'].t1_goals = int(update.message.text)

        bot.send_message(update.message.chat_id,
                         "به نظرت {} چند تا گل میزنه؟"
                         .format(user_temp_data[tg_user.id]['temp_data'].match.teams.all()[1].name),
                         reply_markup=ForceReply())

        if user_temp_data[tg_user.id]['temp_data'].match.is_knockout:
            user_temp_data[tg_user.id]['status'] = STATUS_PISHBINI_PT1
        else:
            user_temp_data[tg_user.id]['status'] = STATUS_PISHBINI_FINAL

    @staticmethod
    def pishbini_pt1(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        user_temp_data[tg_user.id]['temp_data'].t2_goals = int(update.message.text)

        bot.send_message(update.message.chat_id,
                         "به نظرت {} تو پنالتی چند تا گل میزنه؟"
                         .format(user_temp_data[tg_user.id]['temp_data'].match.teams.all()[0].name),
                         reply_markup=ForceReply())

        user_temp_data[tg_user.id]['status'] = STATUS_PISHBINI_PT2

    @staticmethod
    def pishbini_pt2(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        user_temp_data[tg_user.id]['temp_data'].t1_pk_goals = int(update.message.text)

        bot.send_message(update.message.chat_id,
                         "به نظرت {} تو پنالتی چند تا گل میزنه؟"
                         .format(user_temp_data[tg_user.id]['temp_data'].match.teams.all()[1].name),
                         reply_markup=ForceReply())

        user_temp_data[tg_user.id]['status'] = STATUS_PISHBINI_FINAL

    @staticmethod
    def pishbini_final(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        if user_temp_data[tg_user.id]['temp_data'].match.is_knockout:
            user_temp_data[tg_user.id]['temp_data'].t2_pk_goals = int(update.message.text)
        else:
            user_temp_data[tg_user.id]['temp_data'].t2_goals = int(update.message.text)

        if user_temp_data[tg_user.id]['temp_data'].match.time <= datetime.datetime.now(get_current_timezone()):
            bot.send_message(update.message.chat_id, "مهلت برای ثبت پیشبینی به پایان رسیده است.")
            user_temp_data[tg_user.id]['status'] = STATUS_IDLE
            user_temp_data[tg_user.id]['temp_data'] = None
            return

        user_temp_data[tg_user.id]['temp_data'].save()

        bot.send_message(update.message.chat_id, "پیشبینی با موفقیت ثبت شد.")

        user_temp_data[tg_user.id]['status'] = STATUS_IDLE
        user_temp_data[tg_user.id]['temp_data'] = None

    @staticmethod
    def pre_pishbini(bot: Bot, update: Update):
        tg_user: TelegramUser = update.message.from_user
        user = User.objects.get(id=update.message.from_user.id)

        if user_temp_data[tg_user.id]['status'] == STATUS_PRE_PISHBINI:
            # TODO
            # if datetime.datetime.strptime(BEGIN_TIME, "") <= datetime.datetime.now(get_current_timezone()):
            #     bot.send_message(update.message.chat_id, "مهلتت تموم شده.")
            #     user_temp_data[tg_user.id]['status'] = STATUS_IDLE
            #     user_temp_data[tg_user.id]['temp_data'] = None
            #     return
            user.pre_pishbini = update.message.text
            user.save()
            bot.send_message(update.message.chat_id, "پیشبینی با موفقیت ثبت شد.")
            return

        bot.send_message(update.message.chat_id,
                         "پیشبنی کن.",
                         reply_markup=ForceReply())
