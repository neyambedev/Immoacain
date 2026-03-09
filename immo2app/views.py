from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InscriptionForm
from .models import Terrain, ImageTerrain, VideoTerrain
from django.http import JsonResponse
from functools import wraps

def superuser_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('connexion')
        if not request.user.is_superuser:
            from django.shortcuts import redirect
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper

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



def _valider_video(fichier):
    """
    Valide qu'un fichier uploadé est bien une vidéo autorisée.
    Retourne (True, None) si valide, (False, message_erreur) sinon.
    """
    import os

    MAX_VIDEO_MB = 15
    ALLOWED_VIDEO_EXT  = ['.mp4', '.mov', '.avi', '.webm', '.mkv']
    ALLOWED_VIDEO_MIME = ['video/mp4', 'video/quicktime', 'video/x-msvideo',
                          'video/webm', 'video/x-matroska']

    # 1. Taille max 15 Mo
    if fichier.size > MAX_VIDEO_MB * 1024 * 1024:
        return False, f"'{fichier.name}' dépasse {MAX_VIDEO_MB} Mo."

    # 2. Extension
    ext = os.path.splitext(fichier.name)[1].lower()
    if ext not in ALLOWED_VIDEO_EXT:
        return False, f"'{fichier.name}' : extension non autorisée. Utilisez MP4, MOV, AVI, WEBM ou MKV."

    # 3. Type MIME
    if fichier.content_type not in ALLOWED_VIDEO_MIME:
        return False, f"'{fichier.name}' : type de fichier vidéo non reconnu."

    return True, None

@login_required(login_url='connexion')
def ajouter_terrain(request):
    if request.method == 'POST':
        type_bien    = request.POST.get('type_bien')
        prix         = request.POST.get('prix')
        localisation = request.POST.get('localisation')
        quartier     = request.POST.get('quartier')
        description  = request.POST.get('description')
        duree_location  = request.POST.get('duree_location')

        # ── Champs selon le type de bien ───────────────────────
        if type_bien == 'location':
            nom_location       = request.POST.get('nom_location', '').strip()
            categorie_location = request.POST.get('categorie_location', '')
            superficie         = None
            if categorie_location == 'hotel' :
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

        fichiers_images = request.FILES.getlist('images')
        fichiers_videos = request.FILES.getlist('videos')

        # ── Validation : au moins une image ────────────────────
        if not fichiers_images:
            messages.error(request, "Veuillez ajouter au moins une image.")
            return render(request, 'ajouter_terrain.html')

        if len(fichiers_images) > 10:
            messages.error(request, "Maximum 10 images autorisées par bien.")
            return render(request, 'ajouter_terrain.html')

        if len(fichiers_videos) > 3:
            messages.error(request, "Maximum 3 vidéos autorisées par bien.")
            return render(request, 'ajouter_terrain.html')

        for fichier in fichiers_images:
            ok, erreur = _valider_image(fichier)
            if not ok:
                messages.error(request, f"Image refusée — {erreur}")
                return render(request, 'ajouter_terrain.html')

        for fichier in fichiers_videos:
            ok, erreur = _valider_video(fichier)
            if not ok:
                messages.error(request, f"Vidéo refusée — {erreur}")
                return render(request, 'ajouter_terrain.html')

        # ── Création du bien ────────────────────────────────────
        terrain = Terrain.objects.create(
            titre=titre,
            type_bien=type_bien,
            superficie=superficie,
            nom_location=nom_location,
            categorie_location=categorie_location,
            duree_location=duree_location,
            prix=prix,
            localisation=localisation,
            quartier=quartier,
            description=description,
            proprietaire=request.user,
        )

        for fichier in fichiers_images:
            ImageTerrain.objects.create(terrain=terrain, image=fichier)

        for fichier in fichiers_videos:
            VideoTerrain.objects.create(terrain=terrain, video=fichier)

        messages.success(request, "Bien ajouté avec succès ! Il sera publié après validation par un administrateur.")
        return redirect('home')

    return render(request, 'ajouter_terrain.html')

def liste_terrains(request):
    # Récupère uniquement les terrains (type_bien = 'terrain') validés depuis la base
    terrains = Terrain.objects.filter(type_bien='terrain', statut='valide', disponible=True).order_by('-date_ajout')

    # Envoie la liste des terrains au template
    return render(request, 'home.html', {'terrains': terrains})

def liste_maisons(request):
    # Récupère uniquement les maisons (type_bien = 'maison') validées depuis la base
    maisons = Terrain.objects.filter(type_bien='maison', statut='valide', disponible=True).order_by('-date_ajout')

    # Envoie la liste des maisons au template
    return render(request, 'home.html', {'terrains': maisons})

def liste_locations(request):
    locations = Terrain.objects.filter(type_bien='location', categorie_location__in=['appartement', 'chambre'], statut='valide', disponible=True).order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': locations})

def liste_hotels(request):
    hotels_qs = Terrain.objects.filter(
        type_bien='location', categorie_location='hotel', statut='valide', disponible=True, reservee=False
    ).order_by('nom_location', '-date_ajout')

    # Regrouper par nom_location -> liste de dicts pour le template Django
    grouped_dict = {}
    for terrain in hotels_qs:
        nom = (terrain.nom_location or '').strip() or terrain.titre
        if nom not in grouped_dict:
            grouped_dict[nom] = []
        grouped_dict[nom].append(terrain)

    hotels_grouped = [
        {'nom': nom, 'biens': biens, 'count': len(biens)}
        for nom, biens in grouped_dict.items()
    ]

    return render(request, 'liste_hotels.html', {'hotels_grouped': hotels_grouped})



def liste_appartements(request):
    appartements = Terrain.objects.filter(type_bien='location', categorie_location='appartement', statut='valide', disponible=True).order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': appartements})

def liste_chambres(request):
    chambres = Terrain.objects.filter(type_bien='location', categorie_location='chambre', statut='valide', disponible=True).order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': chambres})
def base(request):
    return render(request,'base.html')

def home(request):
    
    terrains = Terrain.objects.filter(statut='valide', disponible=True).order_by('-date_ajout')
    return render(request, 'home.html', {'terrains': terrains})
def footer(request):
    return render(request,'footer.html')
def filtrer_terrains(request):
    q = request.GET.get('q', '')
    categorie = request.GET.get('categorie', '')  # ex: 'appartement,chambre' ou 'hotel'

    terrains = Terrain.objects.filter(statut='valide', disponible=True).prefetch_related('images').select_related('proprietaire')

    if categorie:
        cats = [c.strip() for c in categorie.split(',')]
        terrains = terrains.filter(categorie_location__in=cats)

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

@superuser_required
def moderation_terrains(request):
    """Vue pour afficher tous les terrains en attente de modération"""
    terrains_en_attente = Terrain.objects.filter(statut='en_attente').order_by('-date_ajout')
    terrains_valides    = Terrain.objects.filter(statut='valide').order_by('-date_ajout')[:10]
    terrains_rejetes    = Terrain.objects.filter(statut='rejete').order_by('-date_ajout')[:10]
    biens_masques       = Terrain.objects.filter(statut='valide', disponible=False).order_by('-date_ajout')
    chambres_reservees  = Terrain.objects.filter(
        statut='valide', categorie_location='hotel', reservee=True
    ).order_by('-date_ajout')

    context = {
        'terrains_en_attente':  terrains_en_attente,
        'terrains_valides':     terrains_valides,
        'terrains_rejetes':     terrains_rejetes,
        'biens_masques':        biens_masques,
        'chambres_reservees':   chambres_reservees,
    }
    return render(request, 'moderation.html', context)


@superuser_required
def valider_terrain(request, terrain_id):
    """Vue pour valider un terrain"""
    terrain = get_object_or_404(Terrain, id=terrain_id)
    terrain.statut = 'valide'
    terrain.save()
    messages.success(request, f"Le terrain '{terrain.titre}' a été validé avec succès.")
    return redirect('moderation_terrains')


@superuser_required
def rejeter_terrain(request, terrain_id):
    """Vue pour rejeter un terrain"""
    terrain = get_object_or_404(Terrain, id=terrain_id)
    terrain.statut = 'rejete'
    terrain.save()
    messages.warning(request, f"Le terrain '{terrain.titre}' a été rejeté.")
    return redirect('moderation_terrains')

@superuser_required
def toggle_disponibilite(request, terrain_id):
    """Rendre un bien disponible ou le masquer du marché"""
    terrain = get_object_or_404(Terrain, id=terrain_id)
    terrain.disponible = not terrain.disponible
    terrain.save()
    etat = "disponible sur le marché" if terrain.disponible else "masqué du marché"
    messages.success(request, f"'{terrain.titre}' est maintenant {etat}.")
    return redirect('moderation_terrains')


@superuser_required
def toggle_reservation(request, terrain_id):
    """Marquer une chambre d'hôtel comme réservée ou disponible"""
    terrain = get_object_or_404(Terrain, id=terrain_id, categorie_location='hotel')
    terrain.reservee = not terrain.reservee
    # Si réservée → masquer automatiquement du marché
    if terrain.reservee:
        terrain.disponible = False
    else:
        terrain.disponible = True
    terrain.save()
    etat = "réservée (masquée)" if terrain.reservee else "disponible"
    messages.success(request, f"Chambre '{terrain.titre}' marquée comme {etat}.")
    return redirect('moderation_terrains')


@superuser_required
def modifier_terrain(request, terrain_id):
    terrain = get_object_or_404(Terrain, id=terrain_id)
    if request.method == 'POST':
        terrain.titre             = request.POST.get('titre', terrain.titre).strip()
        terrain.prix              = request.POST.get('prix', terrain.prix).strip()
        terrain.localisation      = request.POST.get('localisation', terrain.localisation).strip()
        terrain.quartier          = request.POST.get('quartier', terrain.quartier).strip()
        terrain.description       = request.POST.get('description', terrain.description).strip()
        terrain.superficie        = request.POST.get('superficie', terrain.superficie)
        terrain.nom_location      = request.POST.get('nom_location', terrain.nom_location)
        terrain.categorie_location= request.POST.get('categorie_location', terrain.categorie_location) or None
        terrain.duree_location    = request.POST.get('duree_location', terrain.duree_location) or None
        terrain.statut            = request.POST.get('statut', terrain.statut)
        terrain.save()
        messages.success(request, f"Le bien '{terrain.titre}' a été modifié avec succès.")
    return redirect('moderation_terrains')
