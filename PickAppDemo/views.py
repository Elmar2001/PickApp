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
            user = User.objects.create_user(username, email, password)
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
            store_user = User.objects.create_user(username, email, password)
            store_user.is_store = True

            store = Store(user=store_user, location=location, logo=logo)
            # store_user.save()
            store.save()
        except IntegrityError:
            return render(request, "PickAppDemo/storeRegister.html", {
                "message": "Username already taken."
            })
        login(request, store_user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "PickAppDemo/storeRegister.html")

