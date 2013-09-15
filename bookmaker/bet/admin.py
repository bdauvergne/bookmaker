from django.contrib import admin

from . import models

admin.site.register(models.Question)
admin.site.register(models.Outcome)
admin.site.register(models.Bet)
