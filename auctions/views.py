from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Bid, Category


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}), max_length=15, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}), min_length=8, max_length=15, label="") 

class CreateForm(forms.Form):
    title = forms.CharField(max_length = 25)
    description = forms.CharField(widget=forms.Textarea(), max_length = 70)
    image_url = forms.CharField(max_length= 200, required=False)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Categories'
    )
    first_Bide = forms.IntegerField()


@login_required(login_url="/login")
def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
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
            return render(request, "auctions/login.html", {
            "form": form
        })
    else:
        return render(request, "auctions/login.html", {
            "form": LoginForm()
        })


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

@login_required(login_url="/login")
def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            


            listing = Listing(title= form.cleaned_data["title"], description=form.cleaned_data["description"], image_url=form.cleaned_data["description"])
            listing.save()        

            first_bid = Bid(listing= listing)
            first_bid.save()
            
            for category in form.cleaned_data["categories"]:
                print(category.name)
                listing.categories.add(category)


            
            
            
            return render(request, "auctions/create.html", {
                "form": form
            }) 
        else:
           return render(request, "auctions/create.html", {
                "form": form
            }) 
    else:
        return render(request, "auctions/create.html", {
            "form": CreateForm()
        })
