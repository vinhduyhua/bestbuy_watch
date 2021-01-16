from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name="index"),
	path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("search/<str:search_item>", views.search, name="search"),
    path("watch", views.watch, name="watch"),
    path("get_watch_status/<str:item_id>", views.get_watch_status, name="get_watch_status"),
    path("get_watch_list", views.get_watch_list, name="get_watch_list")
]