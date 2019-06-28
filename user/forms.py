from django import forms
from .models import *

class UserProfileForm(forms.Form):
    name = forms.CharField(label='name', max_length=30)
    phoneNumber = forms.CharField(label='phone number', max_length=50)
    walletAddress = forms.CharField(label='wallet address', max_length=200)

class UserMypageForm(forms.ModelForm):
    name = forms.CharField(required=False)
    email = forms.CharField(required=False)
    phoneNumber = forms.CharField(required=False)
    nickName = forms.CharField(required=False)
    avatar = forms.CharField(required=False)
    class Meta:
        model = User
        fields = ['name', 'email', 'phoneNumber', 'nickName', 'avatar']

    def update(self, model, commit=True):
        for key in self.cleaned_data.keys():
            if len(self.cleaned_data[key]) !=0:
                setattr(model, key, self.cleaned_data[key])
        self.instance = model

        if commit:
            self.instance.save()
        return self.instance