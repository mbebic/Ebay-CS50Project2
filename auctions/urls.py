from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listing/<int:auctionItem_id>", views.auctionItem, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("editWatchlist/<int:auctionItem_id>", views.editWatchlist, name="editWatchlist"),
    path("removeWatchlist/<int:auctionItem_id>", views.removeWatchlist, name="removeWatchlist"),
    path("addbid/<int:auctionItem_id>", views.addbid, name="addbid"),
    path("addcomment/<int:auctionItem_id>", views.addComment, name="addComment"),
    path("close/<int:auctionItem_id>", views.closeAuction, name="closeAuction"),
]
