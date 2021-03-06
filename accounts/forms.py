from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import UserProfile, ItemData


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Compulsory Field')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Compulsory Field')
    email = forms.EmailField(
        max_length=254, help_text='Required.Enter a valid email address.')
    UID = forms.IntegerField(required=True, help_text='Compulsory Field')
    Branch = forms.CharField(max_length=10, required=True,
                             help_text='Compulsory Field')
    Year = forms.CharField(max_length=10, required=True,
                           help_text='Compulsory Field')
    ContactNo = forms.CharField(max_length=12, required=True, help_text='Compulsory Field')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')


class EditProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'username', 'last_name', 'password')


class UploadForm(ModelForm):

    class Meta:
        model = ItemData
        fields = ['Description', 'Location', 'Image']
