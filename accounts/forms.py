from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import LoginForm, PasswordField
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
# UserModel = get_user_model()


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label=_("First name"))
    last_name = forms.CharField(label=_("Last name"))

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email'
        ]


# class CustomLogin(LoginForm):
#     username = forms.CharField(max_length=30, label='Логин')
#     password = forms.CharField(max_length=30, label='Пароль')

