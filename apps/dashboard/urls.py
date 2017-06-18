from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dashboard', views.success, name="success"),


    url(r'^wish_items/create', views.create, name="create"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^home$', views.home, name = "home"),
    url(r'^create_item$', views.adding_item, name = "item"),
    url(r'^wish_items/item_detail/(?P<id>\d+)$', views.item_detail, name = "item_detail"),
    url(r'^delete/(?P<id>\d+)$', views.delete, name = "delete"),
    url(r'^move_up/(?P<id>\d+)$', views.move_up, name = "move_up"),
    url(r'^remove/(?P<id>\d+)$', views.remove, name = "remove"),
]
