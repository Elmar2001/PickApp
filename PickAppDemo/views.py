from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *


# Create your views here.


def index(request):
    return render(request, "PickAppDemo/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        print("LOGIN")
        print(username)
        print(password)
        print(user)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "PickAppDemo/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "PickAppDemo/login.html")


def categories(request):
    pass


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "PickAppDemo/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            # user = User.objects.create_user(username, email, password)
            # user.is_customer=True;
            user = User(username=username, email=email, is_customer=True)
            user.set_password(password)

            user.save()
        except IntegrityError:
            return render(request, "PickAppDemo/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "PickAppDemo/register.html")


def register_store(request):
    if request.method == "POST":
        username = request.POST["store_username"]
        location = request.POST["location"]
        logo = request.POST["logo"]
        email = request.POST["store_email"]

        # Ensure password matches confirmation
        password = request.POST["store_password"]
        confirmation = request.POST["store_confirmation"]
        if password != confirmation:
            return render(request, "PickAppDemo/storeRegister.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            # store_user = User.objects.create_user(username, email, password)
            store_user = User(username=username, email=email, is_store=True)
            store_user.set_password(password)

            store = Store(user=store_user, location=location, logo=logo)

            store_user.save()
            store.save()
        except IntegrityError:
            return render(request, "PickAppDemo/storeRegister.html", {
                "message": "Username already taken."
            })
        login(request, store_user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "PickAppDemo/storeRegister.html")


@login_required(login_url='/login')
def create(request):
    if request.method == "GET":
        return render(request, "PickAppDemo/create.html")

    store_user = request.user
    title = request.POST.get("title")
    image = request.POST.get("image")
    content = request.POST.get("content")
    price = request.POST.get("price")
    stock = request.POST.get("stock")
    category = request.POST.get("category")

    if image == "":
        image = "https://i.imgur.com/GQPN5Q9.jpg"

    if price == "":
        price = 0

    if stock == "":
        stock = 0

    store = Store.objects.get(user=store_user)
    new_listing = Listing(store=store, title=title, image=image, content=content, price=price,
                          stock=stock, category=category)

    new_listing.save()
    # messages.add_message(request, messages.SUCCESS, "Listing created")
    return HttpResponseRedirect(reverse("view", args=(new_listing.pk,)))


def view_listing(request, pid):
    listing = Listing.objects.get(pk=pid)
    print("pid", pid)

    return render(request, "PickAppDemo/listing.html", {
        "listing": listing,
    })


def orders(request):
