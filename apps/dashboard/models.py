# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..user_app.models import User




class ItemManager(models.Manager):
    def add_item(self, item, userID):
        response={}
        errors=[]
        if Item.objects.filter(item_name = item):
            #item = request.post['item']: name we gave in html
            errors.append("Sorry that item exists")
        if len(item) < 3:
            errors.append("Invalid Item! Item should not be less than 3 characters")
        if errors:
            response['status'] = False
            response['errors'] = errors
        else:
            response['status']=True
            response['items'] = Item.objects.create(item_name=item, created_by=User.objects.get(id = userID))
            response['items'].wished_by.add(User.objects.get(id = userID))
        return response

    def item_detail(self, UserID):
        return self.get(id = UserID)

    def delete (self, id):
        self.get(id = id).delete()





class Item(models.Model):
    item_name= models.CharField(max_length =225)
    created_by= models.ForeignKey(User, related_name="created")
    wished_by=models.ManyToManyField(User, related_name="wished")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = ItemManager()
