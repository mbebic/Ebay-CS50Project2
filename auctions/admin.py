from django.contrib import admin
from .models import User, Category, AuctionItem, userComment, userBid

# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(AuctionItem)
admin.site.register(userComment)
admin.site.register(userBid)