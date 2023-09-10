from django.db import models
from django.contrib.auth.models import User
import os

class Medicines(models.Model):
    title = models.CharField(max_length=50, blank=False, default='')
    price = models.CharField(max_length=20, blank=False)


class CartItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)