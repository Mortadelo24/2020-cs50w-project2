from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/",include([
        path("<int:listing_id>", views.listing, name= "listing"),
        path("<int:listing_id>/bid", views.newbid, name="newbid"),
        path("<int:listing_id>/add", views.add_to_watchlist, name="add_to_watchlist"),
        path("<int:listing_id>/remove", views.remove_from_watchlist, name="remove_from_watchlist"),
        path("<int:listing_id>/close", views.close, name="close"),
        path("<int:listing_id>/comment", views.new_comment, name="new_comment")
    ]) ),
    path("categories/", include([
        path("", views.categories , name = "categories"),
        path("<int:category_id>", views.categories , name = "categories"),
        
        
    ])),
    path("watchlist", views.watchlist, name="watchlist")
    
]
