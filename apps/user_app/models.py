# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import date

import re, md5
import binascii
from os import urandom

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$')

# Create your models here.
class UserManager(models.Manager):
    def addUser(self, person):
        response = {}
        errors = []
        if person['name'] == "" or person['username'] =="" or person["password"] == "" or person['confirm_pw'] =="" or person['date'] == "":
            errors.append("one or more field above is empty! Please fill out all the information to register!")
        if len(person["name"])<4 or len(person["username"]) < 4:
            errors.append("Name and username needs to be more than 3 characters")
        if User.objects.filter(username = person['username']):
            errors.append("Sorry that username is taken")
        if len(person["password"]) < 8:
            errors.append("password must be longer than 8 characters")
        if not PW_REGEX.match(person["password"]):
            errors.append("Password should be min. 8 characters, 1 alphabet, & 1 number")
        if not (person["password"]) == (person["confirm_pw"]):
            errors.append("passwords must match!")
        if person['date'] > str(date.today()):
            errors.append("Hired date must be from past!")
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            salt = binascii.b2a_hex(urandom(15))
            hashed_pw = md5.new(person["password"]+salt).hexdigest()
            response['status'] = True
            response['person'] = User.objects.create(name=person["name"], username=person["username"], password =hashed_pw, date=person['date'], salt=salt)
        return response

    def ValUser(self, person):
        response = {}
        errors = []

        try:
            user= User.objects.get(username = person["username"])
            hashed_pw = md5.new(person["password"]+user.salt).hexdigest()

            if user.password == hashed_pw:
                response ["status"]= True
                response ["user"]= user
                return response
            else:
                response ["status"] = False
                return response
        except:
            response ["status"] = False
            return response



class User(models.Model):
    name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    password=models.CharField(max_length=255)
    date = models.DateField('%d-%m-%Y')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    salt = models.TextField()

    objects = UserManager()
