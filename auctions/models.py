from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    image_url = models.CharField(max_length= 200, null=True, default= "https://www.gasso.com/wp-content/uploads/2017/04/noimage.jpg" )
    categories = models.ManyToManyField(Category, related_name="listings")
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    close = models.BooleanField(default = False)

    watchlist_users = models.ManyToManyField(User, related_name="watchlist_listings")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name="bids")
    date = models.DateTimeField(auto_now_add=True)
    price = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")


    def __str__(self):
        return f"{self.price}"
    
    class Meta:
        ordering = ['-date']
    


 


class comment(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    content = models.CharField(max_length = 500)   
    listing = models.ForeignKey(Listing, related_name="comments", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

