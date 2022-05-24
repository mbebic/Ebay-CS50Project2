from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms

from .models import User, AuctionItem, Category, userComment
from .forms import newlistingForm, commentForm, bidForm

def index(request):
    print(AuctionItem.objects.filter(activelisting=True))
    return render(request, "auctions/index.html", {
        "auctionitems": AuctionItem.objects.filter(activelisting=True),
    })

# buttons of active categories on website
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all().order_by('name'),
    })

def category(request, category_id):
    return render(request, "auctions/category.html", {
        "category": Category.objects.get(pk=category_id),
        "auctionitems": AuctionItem.objects.filter(activelisting=True, itemCategory=category_id),
    })

def auctionItem(request, auctionItem_id):
    auctionitem = AuctionItem.objects.get(pk=auctionItem_id)
    comments = userComment.objects.filter(item=auctionItem_id)
    allcomments  = comments.count()

    if request.user.is_authenticated:
        item_inWatchlist = auctionitem.item_inWatchlist(request.user)
    else:
        item_inWatchlist = False

    return render(request, "auctions/listing.html", {
        "auctionitem": auctionitem,
        "bidForm": bidForm(),
        "commentForm": commentForm(),
        "auctionItem_id": auctionItem_id,
        "comments": comments,
        "allcomments": allcomments,
        "item_inWatchlist": item_inWatchlist,
        "user": request.user
    })

@login_required(login_url="login")
def newlisting(request):
    if request.method == "POST":
        form = newlistingForm(request.POST, request.FILES) # saves user input into form

        if form.is_valid():
            form.instance.author = request.user
            new_auctionItem = form.save()
            return HttpResponseRedirect(reverse("listing", args=(new_auctionItem.pk,)))

    else:
        form = newlistingForm() # creates blank form

    return render(request, "auctions/newlisting.html", {
        "form": form
    })

@login_required(login_url="login")
def editWatchlist(request, auctionItem_id):
    if request.method == "POST":
        user = request.user
        auctionitem = AuctionItem.objects.get(pk=auctionItem_id)

        # removes item from watchlist if user has it
        if auctionitem.item_inWatchlist(user):
            auctionitem.watchedby.remove(user)
        else:
            # adds item to watchlist if user does not have it
            user.watchlist.add(auctionitem)
        
        return HttpResponseRedirect(reverse("listing", args=(auctionItem_id,)))

@login_required(login_url="login")
def removeWatchlist(request, auctionItem_id):
    if request.method == "POST":
        user = request.user
        auctionitem = AuctionItem.objects.get(pk=auctionItem_id)

        auctionitem.watchedby.remove(user)
        return HttpResponseRedirect(reverse("watchlist"))

@login_required(login_url='login')
def watchlist(request):

    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.watchlist.all()
    })

@login_required(login_url="login")
def addbid(request, auctionItem_id):
    if request.method == "POST":
        auctionitem = AuctionItem.objects.get(pk=auctionItem_id)
        form = bidForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.instance.item = auctionitem
            
            if form.instance.bidAmount > auctionitem.current_bid():
                form.save()
                return HttpResponseRedirect(reverse("listing", args=(auctionItem_id,)))
            else:
                return HttpResponseRedirect(reverse("listing", args=(auctionItem_id,)))

@login_required(login_url="login")
def addComment(request, auctionItem_id):
    if request.method == "POST":
        auctionitem = AuctionItem.objects.get(pk=auctionItem_id)
        form = commentForm(request.POST)

        if form.is_valid():
            form.instance.user = request.user
            form.instance.item = auctionitem
            form.save()

            return HttpResponseRedirect(reverse("listing", args=(auctionItem_id,)))
            
@login_required(login_url="login")
def closeAuction(request, auctionItem_id):
    # closes auction that user created
    if request.method == "POST" and AuctionItem.objects.get(pk=auctionItem_id).author == request.user:
        AuctionItem.objects.filter(pk=auctionItem_id).update(activelisting=False)
        return redirect("/")

    else:
        return render(request, "auctions/error.html", {
            "message": "You are not the creator of this item. You can not end the auction."
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
