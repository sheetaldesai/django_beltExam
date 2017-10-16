# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *
import re
import bcrypt
from django.utils import timezone
from django.contrib import messages

# Create your views here.
def index (request) :
    # context = {'users': Users.objects.all()}
    # print context
    # request.session.flush()
    context = {}
    storage = messages.get_messages(request)
    for message in storage :
        print "message: ", message.message
        if 'name' in message.tags :
            context['name'] = message.message
        elif 'alias' in message.tags :
            context['username'] = message.message

    print "Index context: ", context
    return render(request, 'wishListApp/index.html', context)

def register(request) :
    error = False
    context = {}
    print "in register"
    # print "request.post: ", request.POST 
    if request.method == "POST":
        password = request.POST['password']
        c_password = request.POST['confirm_password']
        print "Post: ", request.POST
        # if re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password)):
        #     request.Flash['invalid_password'] = "The password must be at least 8 characters long"
        #     print "password invalid"
        #     return redirect(reverse("bookReviews:home"))
    
        if len(password) < 8:
            messages.add_message(request, messages.ERROR, 'Passwords do not match.')
            print "password less than 8"
            error = True
        if password != c_password :
            messages.add_message(request, messages.ERROR, 'Password has to be mininum 8 characters long')
            print "password mismatch"
            error = True
        try: 
            user = Users.objects.get(name = request.POST['name'])
            print "user: ", user
            messages.add_message(request, messages.ERROR, 'User with this name already exists. Please log in', extra_tags="register")
            print "user exists"
            error = True
        except Users.DoesNotExist:
            if not error:
                # encrypt the password
                hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
                Users.objects.create(name=request.POST['name'], username=request.POST['username'], password = hash1, data_hired=request.POST['hire_date'])
                messages.add_message(request, messages.INFO, "Registration successful! Please log in", extra_tags="register_successful")
                print "added user"
      
    if error :
        messages.add_message(request, messages.INFO, request.POST['name'], extra_tags = 'name')
        messages.add_message(request, messages.INFO, request.POST['username'], extra_tags = 'username') 
    
    return redirect(reverse('wishList:home'))
        
def login (request):
    if request.method == "POST":
        password = request.POST['login_password']
        username = request.POST['login_username']
        print "username {} password {}".format(username, password)
       
        try :
            user = Users.objects.get(username = username)
            print user
            print user.password
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                print "password match"
                request.session['logged_in_user'] = user.id
                print "logged in user: ",request.session['logged_in_user']
                return redirect(reverse('wishList:dashboard'))
            else: 
                print "password mismatch"
                messages.add_message(request, messages.ERROR, 'Incorrect User Id or Password. Please try again')
                return redirect(reverse('wishList:home'))
        except Users.DoesNotExist:
            print "email not found"
            messages.add_message(request, messages.ERROR, 'Incorrect User Id or Password. Please try again')
            return redirect(reverse('wishList:home'))

def logout (request) :
    request.session.flush()
    return redirect(reverse('wishList:home'))

def dashboard(request) :
    user_name = Users.objects.get(pk=int(request.session['logged_in_user'])).name
    print "user name: ", user_name
    log = 'Logout'
    wishList = WishList.objects.all()
    # books = Books.objects.all()
    # print "Books: ", books
    context = {
        'user_name': user_name,
        'log':log,
        'wishList':wishList,
        # 'books':books
    }
    return render(request, 'wishListApp/dashboard.html', context)

def createWishList(request) :
    context = {}
    return render(request, 'wishListApp/createWishList.html', context)

def addWishList(request) :
    context = {}
    if request.method == "POST":
        print request.POST
        user = Users.objects.get(pk=int(request.session['logged_in_user']))
        item = Items.objects.create(nane=request.POST['name'],creator=user, date_created = timezone.now())
    HttpResponse("added")

