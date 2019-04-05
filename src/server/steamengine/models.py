from __future__ import unicode_literals
from django.db import models
from django.db import connection

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    steam_id = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
