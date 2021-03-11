from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__" # ["username", "email", "password1", "password2"]


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"