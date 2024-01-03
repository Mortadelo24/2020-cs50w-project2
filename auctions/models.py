from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length = 25)
    description = models.CharField(max_length = 70)
    image_url = models.CharField(max_length= 200, null=True)
    categories = models.ManyToManyField(Category, related_name="listings")

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, related_name="bids")


class comments(models.Model):
    pass   

