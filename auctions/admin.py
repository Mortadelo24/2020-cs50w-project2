from django.contrib import admin

from .models import Category, Bid, Listing

admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Listing)