from django.db import models
from django.contrib.auth.models import User
import os

class Medicines(models.Model):
    title = models.CharField(max_length=50, blank=False, default='')
    price = models.CharField(max_length=20, blank=False)


class CartItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.CharField(max_length=20, blank=False)

class Stock(models.Model):
    title = models.CharField(max_length=50, blank=False, default='', primary_key=True)
    price = models.CharField(max_length=20, blank=False)
    category = models.CharField(max_length=40, blank=False)
    description = models.CharField(max_length=100, blank=False)

class Order(models.Model):
    orderid = models.CharField(max_length=50, blank=False, default='')
    title = models.CharField(max_length=50, blank=False, default='')
    price = models.CharField(max_length=20, blank=False)
    quantity = models.CharField(max_length=10, blank=False, default='')
    date = models.CharField(max_length=30, blank=False, default='')