from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.core.validators import MinValueValidator


from .models import User, Listing, Bid, Category, Comment


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}), max_length=15, label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}), min_length=8, max_length=15, label="") 

class CreateForm(forms.Form):
    title = forms.CharField(max_length = 100)
    description = forms.CharField(widget=forms.Textarea(), max_length = 500)
    image_url = forms.CharField(max_length= 200, required=False, )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Categories',
        required=False
    )
    first_Bide = forms.IntegerField()



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

       
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if not (username and email and password and confirmation):
            return render(request, "auctions/register.html", {
                "message": "you have to complete the form"
            })



         # Ensure password matches confirmation
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
            


            listing = Listing(user= request.user , title= form.cleaned_data["title"], description=form.cleaned_data["description"])
            
            if form.cleaned_data["image_url"]:
                listing.image_url = form.cleaned_data["image_url"]
            
            listing.save()        

            first_bid = Bid(user= request.user, listing = listing, price = form.cleaned_data["first_Bide"] )
            first_bid.save()
            
            for category in form.cleaned_data["categories"]:
                listing.categories.add(category)


            
            
            
            return HttpResponseRedirect(reverse("listing",args=(listing.id,)))
        else:
           return render(request, "auctions/create.html", {
                "form": form
            }) 
    else:
        return render(request, "auctions/create.html", {
            "form": CreateForm()
        })


def index(request):
    
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(close = False)
    })
def categories(request, category_id = None):
    
    categories = Category.objects.all()

    if category_id:
        try:
            category = Category.objects.get(pk = category_id)
        except KeyError:
            return HttpResponseBadRequest("Bad Request: no category chosen")
        except Category.DoesNotExist:
            return HttpResponseBadRequest("Bad Request: category does not exist")
        
        return render(request, "auctions/categories.html", {
            "categories" : categories,
            "category": category
        })
        

        



    return render(request, "auctions/categories.html", {
        "categories" : categories,
    })






def listing(request, listing_id):
    try:
         listing =  Listing.objects.get(pk=listing_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no listing chosen")
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")


   
    return render(request, "auctions/listing.html",{
        "listing": listing,
    })

@login_required(login_url="/login")
def newbid(request, listing_id):
    if request.method == "POST":
        price = int(request.POST["price"])
        if price:
            try:
                listing = Listing.objects.get(pk = listing_id)
            except KeyError:
                return HttpResponseBadRequest("Bad Request: no listing chosen")
            except Listing.DoesNotExist:
                return HttpResponseBadRequest("Bad Request: listing does not exist")



            if price <= listing.bids.first().price:
                return HttpResponseBadRequest("Bad Request: your bid has to be higer than the last one")
            elif listing.close:
                return HttpResponseBadRequest("Bad Request: This listing is closed")
           
            bid = Bid(user= request.user, listing= listing , price = price )
            bid.save()


            return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

@login_required(login_url="/login")
def watchlist(request):
    return render(request, "auctions/watchList.html", {
        "listings" : request.user.watchlist_listings.all
    })

@login_required(login_url="/login")
def add_to_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk = listing_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no listing chosen")
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")
    
    listing.watchlist_users.add(request.user)

    listing.save()

    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))

@login_required(login_url="/login")
def remove_from_watchlist(request, listing_id):
    try:
        listing = Listing.objects.get(pk = listing_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no listing chosen")
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")
    
    listing.watchlist_users.remove(request.user)

    listing.save()

    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))
    


@login_required(login_url="/login")
def close(request, listing_id):
    try:
        listing = Listing.objects.get(pk = listing_id)
    except KeyError:
        return HttpResponseBadRequest("Bad Request: no listing chosen")
    except Listing.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: listing does not exist")
    
    if not listing.user == request.user:
        return HttpResponseBadRequest("Bad Request: you are not the owner of this listing, yo can not close it")


    listing.close = True

    listing.save()


    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))
    
    


@login_required(login_url="/login")
def new_comment(request, listing_id):
    if request.method == "POST":
        comment = str(request.POST["comment"])
        if comment and len(comment) > 2 :
            try:
                listing = Listing.objects.get(pk = listing_id)
            except KeyError:
                return HttpResponseBadRequest("Bad Request: no listing chosen")
            except Listing.DoesNotExist:
                return HttpResponseBadRequest("Bad Request: listing does not exist")
            
            comment = Comment(content=comment, listing= listing, user = request.user)

            comment.save()

   


    return HttpResponseRedirect(reverse("listing",args=(listing_id,)))
    