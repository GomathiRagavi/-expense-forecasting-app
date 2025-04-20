

# Create your models here.
from django.db import models

class Expense(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=50)
    item = models.CharField(max_length=100)
    amount = models.FloatField()

