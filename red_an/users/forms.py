from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class UserLoginForm(forms.Form):
    username = forms.CharField(label='Username', required=True)
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)

    def clean(self):
        data = self.cleaned_data
        username = data.get('username')
        password = data.get('password1')
        user = authenticate(username=username, password=password)
        if user is None:
            self.add_error('username', 'username or password are incorrect')
        return data


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Username', min_length=5, max_length=150)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter your username',
            'title': 'From 5 to 150 characters. Letters, digits and @/./+/-/_ only. Case insensitive'
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': '*****',
            'title': "Can't be too similar to other personal information,\nMust contain at least 8 characters,\nCan't be a commonly user password,\nCan't be entirely numeric"
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': '*****',
            'title': 'Please, repeat your password'
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Enter your email address',
            'title': 'example@email.com'
        })

    field_order = ['username', 'email', 'password1', 'password2']
