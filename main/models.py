from django.db import models

"""
Assumptions:
1. Vending machine has unlimited stocks and cash notes.
"""

class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    price = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
