# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-17 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishListApp', '0002_auto_20171017_0500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='item',
        ),
        migrations.RemoveField(
            model_name='wishlist',
            name='owner',
        ),
        migrations.AddField(
            model_name='items',
            name='wisher',
            field=models.ManyToManyField(to='wishListApp.Users'),
        ),
        migrations.DeleteModel(
            name='WishList',
        ),
    ]