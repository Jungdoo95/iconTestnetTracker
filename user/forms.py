from django import forms

class UserProfileForm(forms.Form):
    name = forms.CharField(label='name', max_length=30)
    phoneNumber = forms.CharField(label='phone number', max_length=50)
    walletAddress = forms.CharField(label='wallet address', max_length=200)