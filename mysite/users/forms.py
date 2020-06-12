from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, label='First Name', widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(max_length=100, label='Last Name', widget=forms.TextInput(attrs={'class': 'input'}))
    email = forms.EmailField(max_length=150, label='Email', widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'input'}))

    # image = forms.FileField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'input'}),

            # 'first_name': forms.CharField(attrs={'class': 'input', 'required': True}),
            # 'last_name': forms.CharField(attrs={'class': 'input', 'required': True}),
            # 'email': forms.EmailInput(attrs={'class': 'input', 'required': True}),
        }


class UserEditForm(UserChangeForm):
    is_moderator = forms.BooleanField

    class Meta:
        model = User
        fields = '__all__'
