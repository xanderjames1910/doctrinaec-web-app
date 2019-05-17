from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailInput()

    class Meta():
        model = User
        fields =  ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de Usuario'
        self.fields['username'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ingresa tu nombre de usuario',
        }
        self.fields['email'].label = 'Dirección de correo'
        self.fields['email'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo electrónico',
        }
