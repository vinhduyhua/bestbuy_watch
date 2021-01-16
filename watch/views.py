import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Item, Watchlist


@login_required(login_url="login")
def index(request):
	items = Item.objects.all()
	return render(request, "watch/index.html")

# Search item
def search(request, search_item):
	found_items = []
	items = Item.objects.all()
	for item in items:
		search_item = search_item.lower()
		item_title = item.title.lower()
		if item_title.find(search_item) != -1:
			found_items.append(item.serialize())

	return JsonResponse(found_items, safe=False)

# Add item to watch list and display watch list
@csrf_exempt
def watch(request):

	if request.method == "POST":

		data = json.loads(request.body)
		item_id = data.get("item_id")
		item = Item.objects.get(pk=int(item_id))

		if Watchlist.objects.filter(user=request.user, items=item).exists():
			watch = Watchlist.objects.get(user=request.user, items=item)
			if watch.watched:
				watch.watched = False
			else:
				watch.watched = True
			watch.save()
		else:
			watch = Watchlist(
				user = request.user,
				items = item,
				)
			watch.save()

		return HttpResponseRedirect(reverse("index"))

	else:
		return render(request,'watch/watchlist.html')

def get_watch_status(request, item_id):

	item = Item.objects.get(pk=int(item_id))

	if Watchlist.objects.filter(user=request.user, items = item).exists():
		watched_item = Watchlist.objects.get(user=request.user, items = item)
		if watched_item.watched:
			return HttpResponse('True')
		else:
			return HttpResponse('False')
	else:
		return HttpResponse('False')

def get_watch_list(request):

	watched_items = []

	if Watchlist.objects.filter(user=request.user, watched=True).exists():
		for item in Watchlist.objects.filter(user=request.user, watched=True):
			watched_items.append(item.serialize())

	return JsonResponse(watched_items, safe=False)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "watch/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "watch/login.html")

def register(request):
	if request.method == "POST":
	    username = request.POST["username"]
	    email = request.POST["email"]

	    # Ensure password matches confirmation
	    password = request.POST["password"]
	    confirmation = request.POST["confirmation"]
	    if password != confirmation:
	        return render(request, "watch/register.html", {
	            "message": "Passwords must match."
	        })

	    # Attempt to create new user
	    try:
	        user = User.objects.create_user(username, email, password)
	        user.save()
	    except IntegrityError:
	        return render(request, "watch/register.html", {
	            "message": "Username already taken."
	        })
	    login(request, user)
	    return HttpResponseRedirect(reverse("index"))
	else:
	    return render(request, "watch/register.html")

