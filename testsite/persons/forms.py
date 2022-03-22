from django import forms
from . import models
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="Login",widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter your nickname", 'type': 'text', 'style':'margin-bottom: -1px;border-bottom-right-radius: 0;border-bottom-left-radius: 0;'}))
    password = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)


    class Meta:
        model = User
        fields = ('username', 'first_name','last_name', 'email', 'password1', 'password2')


    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
