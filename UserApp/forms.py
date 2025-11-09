from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
class userRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','nationality','affiliation','password1','password2']
        widgets = {
            'email':forms.EmailInput(),
            'password1':forms.PasswordInput(),
            }