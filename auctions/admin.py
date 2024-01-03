from django.contrib import admin

from .models import Category, Bid, Listing, Comment, User

admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(User)