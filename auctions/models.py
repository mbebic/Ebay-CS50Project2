from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db.models import Max
from django.forms import ModelForm

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

class AuctionItem(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(4)])
    description = models.CharField(max_length=2000, validators=[MinLengthValidator(30)])
    startBid = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000000000)])
    image = models.ImageField(upload_to='uploads/', height_field=None, width_field=None)
    itemCategory = models.ForeignKey(Category, on_delete=models.CASCADE, default="", blank=True, null=True)
    activelisting = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctionitems")
    timePosted = models.DateTimeField(auto_now_add=True)
    watchedby = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title}"

    def num_bids(self):
        return self.bid.count()

    def current_bid(self):
        if self.num_bids() > 0:
            return (self.bid.aggregate(Max('bidAmount'))['bidAmount__max'])
        else:
            return self.startBid

    def current_winBid(self):
        if self.num_bids() > 0:
            return self.bid.get(bidAmount=self.current_bid()).user
        else: 
            return None

    def item_inWatchlist(self, user):
        return user.watchlist.filter(pk=self.pk).exists()

class userComment(models.Model):
    comment = models.CharField(max_length=2000, validators=[MinLengthValidator(4)])
    timeofComment = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")

    def __str__(self):
        return str(self.comment)

class userBid(models.Model):
    bidAmount = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000000000)])
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid")

    def __str__(self):
        return str(self.bidAmount)