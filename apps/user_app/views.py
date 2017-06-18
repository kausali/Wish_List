from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "user_app/index.html")

def register(request):

    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Sorry, gotta add something!")
        return redirect("/")

    person = {
    "name" : request.POST["name"],
    "username" : request.POST["username"],
    "password" : request.POST["password"],
    "confirm_pw" : request.POST["confirm_pw"],
    "date": request.POST['date']
    }

    response = User.objects.addUser(person)
    if response['status'] == False:
        for error in response['errors']:
            print error
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        messages.add_message(request, messages.SUCCESS, "You have registered!" )
        request.session["name"]=person["name"]
        request.session["id"]=response["person"].id
        return redirect('items:success')
        # items represents project level url namespace and success is the function in views.py


def login(request):
    if request.method != "POST":
        messages.add_message(request, messages.ERROR, "Wrong path")
        return redirect("/")

    person = {
    "username" : request.POST["username"],
    "password" : request.POST["password"],
    }

    response = User.objects.ValUser(person)

    if response ["status"]:
        request.session["name"]=response["user"].name
        request.session["id"]=response["user"].id
        # return redirect("secrets:success")
        return redirect('items:success')
    else:
        messages.add_message(request, messages.ERROR, "Username/password field cannout be blank!")
        return redirect("/")
