from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="Имя пользователя:",
        widget=forms.TextInput,
    )
    email = forms.EmailField(
        label="Электронная почта:",
        widget=forms.EmailInput,
    )
    password1 = forms.CharField(
        label="Пароль:",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Повтор пароля:",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Это имя пользователя уже используется.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот электронный адрес уже используется.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')

class LoginForm(AuthenticationForm):
    pass