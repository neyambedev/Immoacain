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
            user.email      = form.cleaned_data.get('email')
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



def _valider_image(fichier):
    """
    Valide qu'un fichier uploadé est bien une image autorisée.
    Retourne (True, None) si valide, (False, message_erreur) sinon.
    """
    import os
    from django.conf import settings

    # 1. Vérification taille (5 Mo max)
    max_bytes = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024
    if fichier.size > max_bytes:
        return False, f"'{fichier.name}' dépasse {settings.MAX_IMAGE_SIZE_MB} Mo."

    # 2. Vérification extension
    ext = os.path.splitext(fichier.name)[1].lower()
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        return False, f"'{fichier.name}' : extension non autorisée. Utilisez JPG, PNG ou WEBP."

    # 3. Vérification du type MIME réel (content_type envoyé par le navigateur)
    if fichier.content_type not in settings.ALLOWED_IMAGE_TYPES:
        return False, f"'{fichier.name}' : type de fichier non autorisé."

    # 4. Vérification de la signature magique (magic bytes) — lit les 12 premiers octets
    header = fichier.read(12)
    fichier.seek(0)  # remet le curseur au début pour que Django puisse sauvegarder

    signatures = {
        b'\xff\xd8\xff':           'jpeg',   # JPEG
        b'\x89PNG\r\n\x1a\n':     'png',    # PNG
        b'RIFF':                   'webp',   # WEBP (commence par RIFF....WEBP)
    }

    valide = False
    for sig in signatures:
        if header.startswith(sig):
            # Cas WEBP : vaut aussi vérifier la présence de "WEBP" à l'offset 8
            if sig == b'RIFF':
                if header[8:12] == b'WEBP':
                    valide = True
            else:
                valide = True
            break

    if not valide:
        return False, f"'{fichier.name}' : le contenu du fichier ne correspond pas à une image valide."

    return True, None


@login_required(login_url='connexion')
def ajouter_terrain(request):
    if request.method == 'POST':
        type_bien    = request.POST.get('type_bien')
        prix         = request.POST.get('prix')
        localisation = request.POST.get('localisation')
        quartier     = request.POST.get('quartier')
        description  = request.POST.get('description')

        # ── Champs selon le type de bien ───────────────────────
        if type_bien == 'location':
            nom_location       = request.POST.get('nom_location', '').strip()
            categorie_location = request.POST.get('categorie_location', '')
            superficie         = None

            if not nom_location:
                messages.error(request, "Veuillez saisir le nom de la location.")
                return render(request, 'ajouter_terrain.html')
            if not categorie_location:
                messages.error(request, "Veuillez sélectionner une catégorie.")
                return render(request, 'ajouter_terrain.html')

            # Titre automatique : "Appartement à N'Djamena - Gassi"
            label_cat = dict(Terrain.CATEGORIE_LOCATION_CHOICES).get(categorie_location, categorie_location)
            titre = f"{label_cat} à {localisation} - {quartier}"
        else:
            superficie         = request.POST.get('superficie', '').strip()
            nom_location       = None
            categorie_location = None
            titre = f"{type_bien.capitalize()} à {localisation} - {quartier}"

        fichiers = request.FILES.getlist('images')

        # ── Validation images ───────────────────────────────────
        if not fichiers:
            messages.error(request, "Veuillez ajouter au moins une image.")
            return render(request, 'ajouter_terrain.html')

        if len(fichiers) > 10:
            messages.error(request, "Maximum 10 images autorisées par bien.")
            return render(request, 'ajouter_terrain.html')

        for fichier in fichiers:
            ok, erreur = _valider_image(fichier)
            if not ok:
                messages.error(request, f"Image refusée — {erreur}")
                return render(request, 'ajouter_terrain.html')

        # ── Création du bien ────────────────────────────────────
        terrain = Terrain.objects.create(
            titre=titre,
            type_bien=type_bien,
            superficie=superficie,
            nom_location=nom_location,
            categorie_location=categorie_location,
            prix=prix,
            localisation=localisation,
            quartier=quartier,
            description=description,
            proprietaire=request.user,
        )

        for fichier in fichiers:
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
    locations = Terrain.objects.filter(type_bien='location', statut='valide').order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': locations})

def liste_hotels(request):
    hotels = Terrain.objects.filter(type_bien='location', categorie_location='hotel', statut='valide').order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': hotels})

def liste_appartements(request):
    appartements = Terrain.objects.filter(type_bien='location', categorie_location='appartement', statut='valide').order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': appartements})

def liste_chambres(request):
    chambres = Terrain.objects.filter(type_bien='location', categorie_location='chambre', statut='valide').order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': chambres})
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
            'superficie': terrain.superficie or '',
            'nom_location': terrain.nom_location or '',
            'categorie_location': terrain.get_categorie_location_display() if terrain.categorie_location else '',
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