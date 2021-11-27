# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

class Fruit(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    image = models.CharField(max_length=200, default='https://st2.depositphotos.com/7520316/11068/v/950/depositphotos_110680048-stock-illustration-fruit-icon-fruit-sign.jpg')
    def __str__(self):
        return self.name

class Chat(models.Model):
    author = models.CharField(max_length=200)
    text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.text