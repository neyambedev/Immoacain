from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur, Terrain, ImageTerrain

class InscriptionForm(UserCreationForm):
    username = forms.CharField(label = "Nom d'utilisateur",max_length=30,help_text='')
    prenom = forms.CharField(max_length=50, label="Prénom")
    contact = forms.CharField(max_length=20, label="Contact")
    ville = forms.CharField(max_length=50, label="Ville")
    password1 = forms.CharField(label="Mot de passe",widget=forms.PasswordInput,
    max_length=20)
    password2 = forms.CharField(label="Confirmer le mot de passe",widget=forms.PasswordInput,
    max_length=20,)

    class Meta:
        model = Utilisateur
        fields = ['username', 'prenom', 'contact', 'ville', 'password1', 'password2']
        labels = {'username' : "Nom d'utilisateur" , 
        }


