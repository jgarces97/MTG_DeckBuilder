from django.db import models

# Create your models here.


class Card(models.Model):
    name = models.CharField(max_length=200)
    mana_cost = models.CharField(max_length=20)
    type_line = models.CharField(max_length=200)
    color_identity = models.CharField(max_length=10)
    commander = models.IntegerField()


class Deck(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)