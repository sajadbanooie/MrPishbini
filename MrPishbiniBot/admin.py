from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Pishbini)