from django import forms
from django.contrib.auth.models import User

class LoginForms(forms.Form):
    username = forms.CharField(
        label="Usuário",
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuário',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label="Senha",
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha',
                'class': 'form-control'
            }
        )
    )


    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')

        if username and not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário não cadastrado!')

        return cleaned_data
    

class SignupForms(forms.Form):
    username = forms.CharField(
        label="Usuário",
        required=True,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuário',
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control'
            }
        )
    )

    password = forms.CharField(
        label="Senha",
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Senha',
                'class': 'form-control'
            }
        )
    )

    confirm_password = forms.CharField(
        label="Confirmar Senha",
        required=True,
        max_length=50,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirmar Senha',
                'class': 'form-control'
            }
        )
    )


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Usuário já cadastrado!')
        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email já cadastrado!')
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('As senhas não coincidem')
        
        return cleaned_data