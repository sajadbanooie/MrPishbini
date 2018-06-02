import json

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from telegram import Update, Message
from telegram.bot import Bot

from MrPishbiniBot.bot import MrPishbiniBot
# Create your views here.


@csrf_exempt
def webhook(req: HttpRequest, token: str):
    bot = Bot(token=token)
    update = Update.de_json(json.loads(req.body), bot)

    MrPishbiniBot.update(bot, update)

    return HttpResponse('')
