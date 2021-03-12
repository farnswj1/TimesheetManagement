from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required")
    email = forms.EmailField(max_length=256, required=True, help_text="Required")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_superuser", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required")
    last_name = forms.CharField(max_length=30, required=True, help_text="Required")
    email = forms.EmailField(max_length=256, required=True, help_text="Required")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "is_superuser"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]