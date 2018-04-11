# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ChefIdentity


class ChefIdentityCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = ChefIdentity
        fields = UserCreationForm.Meta.fields
        

class ChefIdentityChangeForm(UserChangeForm):

    class Meta:
        model = ChefIdentity
        fields = UserCreationForm.Meta.fields
