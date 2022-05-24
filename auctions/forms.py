from django import forms
from django.forms import ModelForm
from .models import User, Category, AuctionItem, userComment, userBid

# form for new listing model
class newlistingForm(ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['title', 'description', 'startBid', 'image', 'itemCategory']

# form for new bid on a listing
class bidForm(forms.ModelForm):
    class Meta:
        model = userBid
        fields = ['bidAmount']

# form for new comment on listing
class commentForm(forms.ModelForm):
    class Meta:
        model = userComment
        fields = ['comment']