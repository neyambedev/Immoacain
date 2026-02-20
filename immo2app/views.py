from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm
from .models import Terrain, ImageTerrain
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

def inscription_view(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('prenom')
            user.save()
            messages.success(request, "Inscription réussie ! Vous pouvez maintenant vous connecter.")
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'inscription.html', {'form': form})


def connexion_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            ex=messages.error(request, "Nom d’utilisateur ou mot de passe incorrect.")
    return render(request, 'connexion.html')


def deconnexion_view(request):
    logout(request)
    return redirect('home')


def navigation_view(request):
    return render(request, 'navigation.html')



@login_required(login_url='connexion')
def ajouter_terrain(request):
    if request.method == 'POST':
        type_bien = request.POST.get('type_bien')
        superficie = request.POST.get('superficie')
        prix = request.POST.get('prix')
        localisation = request.POST.get('localisation')
        quartier=request.POST.get('quartier')
        description = request.POST.get('description')
        titre = f"{request.POST['type_bien'].capitalize()} à {request.POST['localisation']} - {request.POST['quartier']}  "

        # On crée d'abord le terrain
        terrain = Terrain.objects.create(
            titre=titre,
            type_bien=type_bien,
            superficie=superficie,
            prix=prix,
            localisation=localisation,
            quartier=quartier,
            description=description,
            proprietaire=request.user ,
        )

        # Puis on ajoute toutes les images uploadées
        for fichier in request.FILES.getlist('images'):
            ImageTerrain.objects.create(terrain=terrain, image=fichier)

        messages.success(request, "Bien ajouté avec succès ! Il sera publié après validation par un administrateur.")
        return redirect('home')

    return render(request, 'ajouter_terrain.html')

def liste_terrains(request):
    # Récupère uniquement les terrains (type_bien = 'terrain') validés depuis la base
    terrains = Terrain.objects.filter(type_bien='terrain', statut='valide').order_by('-date_ajout')

    # Envoie la liste des terrains au template
    return render(request, 'home.html', {'terrains': terrains})

def liste_maisons(request):
    # Récupère uniquement les maisons (type_bien = 'maison') validées depuis la base
    maisons = Terrain.objects.filter(type_bien='maison', statut='valide').order_by('-date_ajout')

    # Envoie la liste des maisons au template
    return render(request, 'home.html', {'terrains': maisons})

def liste_locations(request):
    # Récupère uniquement les locations (type_bien = 'location') validées depuis la base
    locations = Terrain.objects.filter(type_bien='location', statut='valide').order_by('-date_ajout')

    # Envoie la liste des locations au template
    return render(request, 'home.html', {'terrains': locations})
def base(request):
    return render(request,'base.html')

def home(request):
    
    terrains = Terrain.objects.filter(statut='valide').order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': terrains})
def footer(request):
    return render(request,'footer.html')
def filtrer_terrains(request):
    q = request.GET.get('q', '')

    terrains = Terrain.objects.filter(statut='valide').prefetch_related('images').select_related('proprietaire')

    if q:
        terrains = terrains.filter(quartier__icontains=q)

    data = []
    for terrain in terrains:
        data.append({
            'id': terrain.id,
            'titre': terrain.titre,
            'type_bien': terrain.type_bien,
            'localisation': terrain.localisation,
            'prix': terrain.prix,
            'superficie': terrain.superficie,
            'description': terrain.description,
            'quartier': terrain.quartier,
            'proprietaire': terrain.proprietaire.username if terrain.proprietaire else 'N/A',
            'date_ajout': terrain.date_ajout.strftime("%d/%m/%Y %H:%M"),
            'images': [img.image.url for img in terrain.images.all()]
        })

    return JsonResponse({'terrains': data})

# ==================== VUES DE MODÉRATION ====================

@staff_member_required(login_url='connexion')
def moderation_terrains(request):
    """Vue pour afficher tous les terrains en attente de modération"""
    terrains_en_attente = Terrain.objects.filter(statut='en_attente').order_by('-date_ajout')
    terrains_valides = Terrain.objects.filter(statut='valide').order_by('-date_ajout')[:10]
    terrains_rejetes = Terrain.objects.filter(statut='rejete').order_by('-date_ajout')[:10]
    
    context = {
        'terrains_en_attente': terrains_en_attente,
        'terrains_valides': terrains_valides,
        'terrains_rejetes': terrains_rejetes,
    }
    return render(request, 'moderation.html', context)


@staff_member_required(login_url='connexion')
def valider_terrain(request, terrain_id):
    """Vue pour valider un terrain"""
    terrain = get_object_or_404(Terrain, id=terrain_id)
    terrain.statut = 'valide'
    terrain.save()
    messages.success(request, f"Le terrain '{terrain.titre}' a été validé avec succès.")
    return redirect('moderation_terrains')


@staff_member_required(login_url='connexion')
def rejeter_terrain(request, terrain_id):
    """Vue pour rejeter un terrain"""
    terrain = get_object_or_404(Terrain, id=terrain_id)
    terrain.statut = 'rejete'
    terrain.save()
    messages.warning(request, f"Le terrain '{terrain.titre}' a été rejeté.")
    return redirect('moderation_terrains')