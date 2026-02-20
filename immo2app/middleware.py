from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMessageMiddleware:
    """
    Middleware pour afficher un message lorsqu'un utilisateur non connecté
    tente d'accéder à une page protégée
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Vérifier si c'est une redirection vers la page de connexion
        if (response.status_code == 302 and 
            response.url == reverse('connexion') and 
            not request.user.is_authenticated):
            
            # Ajouter le message d'erreur
            messages.error(request, "Veuillez vous connecter à votre compte")
        
        return response
