from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Deck, Card

admin.site.register(Deck)
admin.site.register(Card)