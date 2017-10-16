# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=8)
    data_hired = models.DateTimeField('date hired')
    def __str__(self):
        return "{} {} {} {}".format(self.name, self.username, self.data_hired, self.password) 

class Items(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey('Users', related_name = "created_items", null = True)
    date_created = models.DateTimeField('date created')
    def __str__(self):
        return "{} {}".format(self.name, self.creator.name) 

class WishList(models.Model):
    item = models.ForeignKey('Items', related_name = "wishList", null = True)
    owner = models.ForeignKey('Users', related_name = "my_wishList", null = True)
    
    def __str__(self):
        return "{} {} {}".format(self.item.name, self.item.creator.name, self.owner.name ) 