from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from telegram import Update, Message
from telegram.bot import Bot
# Create your views here.

@csrf_exempt
def webhook(req, token):
    bot = Bot(token=token)
    update = Update.de_json(req.body, bot)
    bot.send_message(update.message.chat_id, "hello")
    return HttpResponse('')
