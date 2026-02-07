from django import forms
from .models import Neighborhood

class RobberyForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'}
            ),
        label="Data",
        required=True,
    )
    time = forms.TimeField(
        widget=forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control'}
            ),
        label="Hora(opcional)",
        required=False,
    )
    street = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Rua'}
        ),
        label="Rua",
        required=True,
    )
    number = forms.CharField(
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Número'}
        ),
        label="Número",
        required=True,
    )
    neighborhood = forms.ModelChoiceField(
        queryset=Neighborhood.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        ),
        label="Bairro",
        required=True,
    )

    description = forms.CharField(
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 2}
        ),
        label="Descrição(opcional)",
        required=False,
    )
