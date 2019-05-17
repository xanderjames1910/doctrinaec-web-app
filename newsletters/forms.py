from django import forms
from .models import NewsLetterUser, Newsletter

class NewsLetterUserSignUpForm(forms.ModelForm):

    class Meta():
        model = NewsLetterUser
        fields = ('name','phone', 'email')

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Nombre:'
        self.fields['phone'].label = 'Teléfono:'
        self.fields['email'].label = 'Dirección de correo:'

class NewsLetterUserUnsubscribeForm(forms.ModelForm):

    class Meta():
        model = NewsLetterUser
        fields = ('email',)

        def clean_email(self):
            email = self.cleaned_data.get('email')

            return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Dirección de correo:'

class NewsLetterCreationForm(forms.ModelForm):

    class Meta():
        model = Newsletter
        fields = ['subject', 'body', 'email', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].label = 'Asunto'
        self.fields['subject'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese el asunto del email',
        }
        self.fields['body'].label = 'Cuerpo del email:'
        self.fields['body'].widget.attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese el cuerpo del email aquí',
            'rows': '10',
        }
        self.fields['email'].label = 'Destinatarios'
        self.fields['status'].label = 'Estado'
