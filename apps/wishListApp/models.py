# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager) :

    def register(self,post):
        errorMsgs = []
        user = {}
        returnVal = {}

        if post['name'] == "" :
            errorMsgs.append({'message': 'Name is required', 'extra_tags':"register"})
        elif len(post['name']) < 3 :
            errorMsgs.append({'message':'Name has to be minimum 3 characters long', 'extra_tags':"register"})
        if post['username'] == "" :
            errorMsgs.append({'message':'username is required', 'extra_tags':"register"})
        elif len(post['username']) < 3 :
            errorMsgs.append({'message':'username has to be minimum 3 characters long', 'extra_tags':"register"})

        if post['password'] == "" :
            errorMsgs.append({'message':'password is required', 'extra_tags':"register"})
        elif len(post['password']) < 8:
            errorMsgs.append({'message':'Password has to be mininum 8 characters long', 'extra_tags':"register"})
            print "password less than 8"      
        elif post['password'] != post['confirm_password'] :
            errorMsgs.append({'message':'Passwords do not match.', 'extra_tags':"register"})
            print "password mismatch"

        try: 
            user = Users.objects.get(username = post['username'])
            print "user: ", user
            errorMsgs.append({'message':'User with {} name already exists. Please select a different username'.format(post['username']), 'extra_tags':"register"})
            print "user exists"
            error = True
        except Users.DoesNotExist:
            if (len(errorMsgs) == 0):
                hash1 = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
                user = Users.objects.create(name=post['name'], username=post['username'], password = hash1, data_hired=post['hire_date'])
                print "added user"
                print "User does not exist"
                
        returnVal = {'user':user,'errors':errorMsgs}
        return returnVal

    def login (self, post) :
        errorMsgs = []
        user = {}

        if post['login_username'] == "" :
            errorMsgs.append({'message':'username is required', 'extra_tags':"login"})
        if post['login_password'] == "" :
            errorMsgs.append({'message':'password is required', 'extra_tags':"login"})
        if (len(errorMsgs) == 0):
            try :
                user = Users.objects.get(username = post['login_username'])
                print user
                print user.password
                if bcrypt.checkpw(post['login_password'].encode(), user.password.encode()):
                    print "login successful"
                else: 
                    print "password mismatch"
                    errorMsgs.append({'message':'Incorrect User Id or Password. Please try again', 'extra_tags':'login'})
            except Users.DoesNotExist:
                print "user not found"
                errorMsgs.appende({'messsage':'Incorrect User Id or Password. Please try again', 'extra_tags':'login'})

        return {'user': user, 'errors': errorMsgs}

class Users(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=8)
    data_hired = models.DateTimeField('date hired')
    objects = UserManager()
    def __str__(self):
        return "{} {} {} {}".format(self.name, self.username, self.data_hired, self.password) 

class Items(models.Model):
    name = models.CharField(max_length=255)
    creator = models.ForeignKey('Users', related_name = "created_items", null = True)
    wisher = models.ManyToManyField(Users)
    date_created = models.DateTimeField('date created')
    def __str__(self):
        return "{} {}".format(self.name, self.creator.name) 

