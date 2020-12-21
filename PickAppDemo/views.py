from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from .models import *


def index(request):
    products = Listing.objects.filter(active=True)  # get only active listings

    return render(request, "PickAppDemo/index.html", {
        "products": products
    })


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
            messages.add_message(request, messages.ERROR, "Sign in unsuccessful")
            return render(request, "PickAppDemo/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "PickAppDemo/login.html")


def logout_view(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Logout successful")
    return HttpResponseRedirect(reverse("index"))


# register functionality for customers
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


# register functionality for stores
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

    if image == "":  # default image if blank
        image = "https://i.imgur.com/GQPN5Q9.jpg"

    if price == "":
        price = 0

    if stock == "":
        stock = 0

    store = Store.objects.get(user=store_user)
    new_listing = Listing(store=store, title=title, image=image, content=content, price=price,
                          stock=stock, category=category)

    new_listing.save()
    messages.add_message(request, messages.SUCCESS, "Listing created")
    return HttpResponseRedirect(reverse("view", args=(new_listing.pk,)))


# view a listing and order
def view_listing(request, pid):
    if request.method == "POST":  # order
        user = request.user
        quantity = int(request.POST.get("quantity"))
        date = request.POST.get("time")
        listing = Listing.objects.get(pk=pid)
        new_order = Orders(user=user, store=listing.store.user, listing=listing, quantity=quantity, date=date)
        new_order.save()
        listing.stock -= quantity  # remove the purchased quantity from stock

        if listing.stock == 0:  # deactivate the listing if stock is zero
            listing.active = False

        listing.save()
        messages.add_message(request, messages.SUCCESS, "Order successful")

        return render(request, "PickAppDemo/listing.html", {
            "listing": listing,
        })

    # view the listing
    listing = Listing.objects.get(pk=pid)
    return render(request, "PickAppDemo/listing.html", {
        "listing": listing,
    })


@login_required(login_url='/login')
def orders(request):
    if request.user.is_customer:  # if the user is a customer
        orders = Orders.objects.filter(user=request.user, completed=False).order_by('-id')

    else:  # the user is a store
        orders = Orders.objects.filter(store=request.user, completed=False).order_by('-id')

    return render(request, "PickAppDemo/orders.html", {
        "orders": orders
    })


# mark order as completed or cancel order
def complete(request, order_id):
    order = Orders.objects.get(pk=order_id)
    order.completed = True

    if request.user.is_customer:  # increase stock if customer cancelled the order
        order.listing.stock += order.quantity
        order.listing.save()

    order.save()
    messages.add_message(request, messages.SUCCESS, "Operation successful")
    return HttpResponseRedirect(reverse("orders"))


# supports searching titles for now
# TODO: add searching other fields
def search(request):
    if request.method == "POST":
        query = request.POST.get("query")
        results = Listing.objects.filter(title=query)
        return render(request, "PickAppDemo/results.html", {
            "results": results
        })

    return render(request, "PickAppDemo/search.html")


# show all categories
def categories(request):
    listings = Listing.objects.all()
    category_list = []

    for listing in listings:
        if listing.category not in category_list and listing.category != "":
            category_list.append(listing.category)

    return render(request, "PickAppDemo/categories.html", {
        "categories": category_list
    })


# see products from a category
def get_category(request, category_name):
    listings = Listing.objects.all()
    list = []

    for l in listings:
        if l.category == category_name and l.active:
            list.append(l)

    return render(request, "PickAppDemo/index.html", {
        "products": list
    })


def store(request, store_name):
    user = User.objects.get(username=store_name)
    store = Store.objects.get(user=user)
    store_listings = Listing.objects.filter(store=store, active=True)  # get active listings of a store

    return render(request, "PickAppDemo/index.html", {
        "products": store_listings
    })
