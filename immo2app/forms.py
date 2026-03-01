from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Terrain, ImageTerrain

FIELD_CLASS = {'class': 'input-field'}

class InscriptionForm(UserCreationForm):
    username  = forms.CharField(
        label="Nom d'utilisateur", max_length=30, help_text='',
        widget=forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': "Choisissez un nom d'utilisateur"})
    )
    prenom = forms.CharField(
        max_length=50, label="Nom complet",
        widget=forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': 'Votre nom complet'})
    )
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={**FIELD_CLASS, 'placeholder': 'exemple@gmail.com'})
    )
    contact = forms.CharField(
        max_length=20, label="Contact",
        widget=forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': '+235 XX XX XX XX'})
    )
    ville = forms.CharField(
        max_length=50, label="Ville",
        widget=forms.TextInput(attrs={**FIELD_CLASS, 'placeholder': "Votre ville (ex: N'Djamena)"})
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={**FIELD_CLASS, 'placeholder': 'Créez un mot de passe'}),
        max_length=128
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={**FIELD_CLASS, 'placeholder': 'Répétez le mot de passe'}),
        max_length=128
    )

    class Meta:
        model  = Utilisateur
        fields = ['username', 'prenom', 'email', 'contact', 'ville', 'password1', 'password2']
        labels = {'username': "Nom d'utilisateur"}
