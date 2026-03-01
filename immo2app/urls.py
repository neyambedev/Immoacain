#urls
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='accueil'),  # URL racine
    path('inscription', views.inscription_view, name='inscription'),
    path('connexion', views.connexion_view, name='connexion'),
    path('deconnexion', views.deconnexion_view, name='deconnexion'),
    path('navigation', views.navigation_view, name='navigation'),
    path('ajouter', views.ajouter_terrain, name='ajouter_terrain'),
    path('lister', views.liste_terrains, name='liste_terrains'),
    path('maisons', views.liste_maisons, name='liste_maisons'),
    path('locations', views.liste_locations, name='liste_locations'),
    path('locations/hotels', views.liste_hotels, name='liste_hotels'),
    path('locations/appartements', views.liste_appartements, name='liste_appartements'),
    path('locations/chambres', views.liste_chambres, name='liste_chambres'),
    path('home', views.home, name='home'),
    path('base', views.base, name='base'),
    path('footer', views.footer, name='footer'),
     path('filtrer_terrains', views.filtrer_terrains, name='filtrer_terrains'),
    
    # URLs de modération (admin uniquement)
    path('/moderation/', views.moderation_terrains, name='moderation_terrains'),
    path('admin/valider/<int:terrain_id>/', views.valider_terrain, name='valider_terrain'),
    path('admin/rejeter/<int:terrain_id>/', views.rejeter_terrain, name='rejeter_terrain'),
    
]