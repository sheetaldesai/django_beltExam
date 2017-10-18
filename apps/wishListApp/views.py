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
    context = {}
    # If we are redirected here from registration/login due to validation errors then pre-populate
    # the name and username fields with the values user entered. 
    storage = messages.get_messages(request)
    for message in storage :
        print "message: ", message.message
        if 'name' in message.tags :
            context['name'] = message.message
        if 'username' in message.tags :
            context['username'] = message.message

    print "Index context: ", context
    return render(request, 'wishListApp/index.html', context)

def register(request) :
    error = False
    context = {}
    print "in register"

    if request.method == "POST":
        print request.POST

        returnVal = Users.objects.register(request.POST)
        if returnVal['user'] :
            request.session['logged_in_user'] = returnVal['user'].id
            print "logged in user: ",request.session['logged_in_user']
            return redirect(reverse('wishList:dashboard'))
        else :
            for error in returnVal['errors'] :
                print error
                messages.error(request,error['message'],extra_tags=error['extra_tags'])
            return redirect(reverse("wishList:home"))

def login (request):
    if request.method == "POST":
        returnVal = Users.objects.login(request.POST)
        if returnVal['user']:
            request.session['logged_in_user'] = returnVal['user'].id
            print "logged in user: ",request.session['logged_in_user']
            return redirect(reverse('wishList:dashboard'))
        else:
            for error in returnVal['errors'] :
                print error
                messages.error(request,error['message'],extra_tags=error['extra_tags'])
            return redirect(reverse('wishList:home'))

def logout (request) :
    request.session.flush()
    return redirect(reverse('wishList:home'))

def dashboard(request) :
    user = __getLoggedUser(request)
    user_name = user.name
    print "user name: ", user_name
    log = 'Logout'
    # Get my wish list items:
    myWishList = user.items_set.all()
    print "myWishList: ", myWishList

    # Other wish list :
    items = Items.objects.all()
    others = []
    for item in items :
        print "item ",item
        # If the item does not have this user as a wisher then add that item
        # to the other list 
        wishers = item.wisher.filter(id = user.id)
        print "wishers {} len {}".format(wishers,len(wishers))
        print wishers
        if (len(wishers) == 0):
            others.append(item)
    
    print others

    context = {
        'user_name': user_name,
        'log':log,
        'wishList':myWishList,
        'others': others
    }
    return render(request, 'wishListApp/dashboard.html', context)

def createWishList(request) :
    context = {}
    
    return render(request, 'wishListApp/createWishList.html', context)

def addNewItem(request) :
    # Create new item and add logged user's wish list 
    if request.method == "POST":
        print request.POST
        if (__validateCreateRequestForm(request)) :
            user = __getLoggedUser(request)
            item = Items.objects.create(name=request.POST['name'],creator=user, date_created = timezone.now())
            item.wisher.add(user)
            item.save()
            print "new item created"
            return redirect(reverse('wishList:dashboard'))
        else :
            print "errors"
            return redirect(reverse('wishList:createWishList'))

def deleteItem(request, itemId) :
    # Delete item.  
    print "in remove, id ",itemId
    item = Items.objects.get(pk=itemId)
    print item
    item.delete()
    return redirect(reverse('wishList:dashboard'))

def addToWishList(request, itemId) :
    # Add item selected from the 'other' table to the logged user's wish list 
    print itemId
    user = __getLoggedUser(request)
    item = Items.objects.get(pk=itemId)
    item.wisher.add(user)
    return redirect(reverse('wishList:dashboard'))

def removeFromWishList(request, itemId) :
    # Remove item from logged user's wish list 
    item = Items.objects.get(pk=itemId)
    user = __getLoggedUser(request)   
    item.wisher.remove(user)

    return redirect(reverse('wishList:dashboard'))

def itemDetails(request, itemId) :
    item = Items.objects.get(pk=itemId)
    wishers = item.wisher.all()
    print wishers
    return render(request, 'wishListApp/itemDetails.html', {'wishers':wishers, 'item': item.name})

def __getLoggedUser(request): 
    user = None
    id = request.session['logged_in_user']
    try:
        user = Users.objects.get(pk=id)
        return user
    except Users.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'You are not logged in. Please log in to continue')
        print "Not logged in"
        return redirect(reverse('wishList:home'))
    return user
            

def __validateLoginForm(request) :
    if request.POST['login_username'] == "" :
        messages.add_message(request, messages.ERROR, 'username is required', extra_tags="login")
    if request.POST['login_password'] == "" :
         messages.add_message(request, messages.ERROR, 'password is required', extra_tags="login")
    if (len(messages.get_messages(request)) > 0):
        print "__validateRegisterForm returning false"
        return False
    else :
        print "__validateRegisterForm returning true"
        return True

def __validateCreateRequestForm(request) :
    if request.POST['name'] == "" :
        messages.add_message(request, messages.ERROR, 'Name is required', extra_tags="createwish")
    elif len(request.POST['name']) < 3 :
        messages.add_message(request, messages.ERROR, 'Name has to be minimum 3 characters long', extra_tags="createwish")
    if (len(messages.get_messages(request)) > 0):
        print "__validateRegisterForm returning false"
        return False
    else :
        print "__validateRegisterForm returning true"
        return True

     



