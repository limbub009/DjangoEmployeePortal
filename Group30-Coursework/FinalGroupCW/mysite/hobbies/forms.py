from django.forms import ModelForm
from hobbies.models import User, extendedUser
from django.forms.widgets import DateInput
from django import forms

class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'city', 'dob']
        labels = {
            'dob': ('Date of Birth:'),
        }
        widgets = {
            'dob': DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput(),
        }
