from django.shortcuts import render, redirect, HttpResponse
from .models import Item
from ..user_app.models import User
from django.contrib import messages


def success(request):
    if not 'id' in request.session:
        messages.add_message(request, messages.ERROR, "Please login.")
        return redirect('/')
    context = {
        'items': Item.objects.filter(wished_by = User.objects.get(id = request.session['id'])),
        'items_wished':Item.objects.exclude(wished_by = User.objects.get(id = request.session['id']))
    }

    return render(request, 'dashboard/index.html', context)

def adding_item(request):
    if request.method == "POST":
        print request.POST['item']
        userID = request.session['id']
        response = Item.objects.add_item(request.POST['item'], userID)

        if response['status'] ==False:
            for error in response['errors']:
                messages.add_message(request, messages.ERROR, error)
            return redirect("items:create")
        else:
            print "YAYYYYYY"
            messages.add_message(request, messages.SUCCESS, "You have successfully added item(s) to your wish list" )
            return redirect("items:success")

    else:
        messages.add_message(request, messages.ERROR, "login/register first")
        return redirect("/")


def create(request):
    if not 'id' in request.session:
        messages.add_message(request, messages.ERROR, "Please login.")
        return redirect('/')
    return render(request, 'dashboard/add.html')


def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "You have logged out!" )
    return redirect("/")


def home(request):
    return redirect("/dashboard")

def item_detail(request, id):
    response = Item.objects.item_detail(id)
    context= {
        'item_detail':response
        }
    return render(request, 'dashboard/each_item.html', context)

def delete (request, id):
    Item.objects.delete(id)
    return redirect('/dashboard')
    #  Item.objects.get(id = id).delete

def move_up(request, id):
    up = Item.objects.get(id = id)
    person = User.objects.get(id = request.session['id'])
    up.wished_by.add(person)
    return redirect('/dashboard')


def remove(request, id):
    rem = Item.objects.get(id = id)
    person = User.objects.get(id = request.session['id'])
    rem.wished_by.remove(person)
    messages.add_message(request, messages.SUCCESS, "You have successfully removed the item from your wishlist " )
    return redirect('/dashboard')
