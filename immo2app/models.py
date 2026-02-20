from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class Utilisateur(AbstractUser):
    Telephone = models.CharField(max_length=20, blank=True, null=True)
    ville = models.CharField(max_length=50, blank=True, null=True)




class Terrain(models.Model):
    TYPE_CHOICES = [
        ('terrain','Terrain'),
        ('maison','Maison'),
        ('location','Location')
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté')
    ]
    type_bien = models.CharField(max_length=200 ,choices=TYPE_CHOICES)
    proprietaire = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="terrains") 
    titre = models.CharField(max_length=200)
    superficie = models.CharField(max_length=100)
    prix = models.CharField(max_length=100)
    localisation = models.CharField(max_length=200)
    quartier = models.CharField(max_length=200)
    description = models.TextField()
    date_ajout = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')


    def __str__(self):
        return self.titre


class ImageTerrain(models.Model):
    terrain = models.ForeignKey(Terrain, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='terrains/')

    def __str__(self):
        return f"Image de {self.terrain.titre}"