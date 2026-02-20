# 🛡️ Système de Modération des Terrains

## ✨ Fonctionnalités ajoutées

### 1. **Système de statut pour les terrains**
Chaque terrain possède maintenant un statut :
- 🕐 **En attente** : Terrain ajouté par un utilisateur, pas encore validé
- ✅ **Validé** : Terrain approuvé par un administrateur, visible sur le site
- ❌ **Rejeté** : Terrain refusé par un administrateur

### 2. **Page de modération (Admin uniquement)**
- URL : `/admin/moderation/`
- Accessible uniquement par les administrateurs (staff)
- Interface avec 3 onglets : En attente, Validés, Rejetés
- Actions : Valider ou Rejeter un terrain en un clic

### 3. **Modifications des vues publiques**
- La page d'accueil affiche uniquement les terrains **validés**
- Les pages de liste (terrains, maisons, locations) affichent uniquement les biens **validés**
- Le filtrage ne retourne que les terrains **validés**

### 4. **Lien de navigation admin**
- Un lien "⚙️ Modération" apparaît dans la navigation pour les administrateurs

---

## 🚀 Installation

### Étape 1 : Appliquer la migration
```bash
python manage.py migrate
```

Cette commande va ajouter le champ `statut` à la table Terrain.

### Étape 2 : Mettre à jour les terrains existants (optionnel)
Si vous avez déjà des terrains dans votre base de données, vous devez les marquer comme validés :

```bash
python manage.py shell
```

Puis dans le shell Django :
```python
from immo2app.models import Terrain

# Marquer tous les terrains existants comme validés
Terrain.objects.all().update(statut='valide')

# Ou marquer comme en attente si vous voulez les revoir
# Terrain.objects.all().update(statut='en_attente')

exit()
```

### Étape 3 : Créer un compte administrateur
Si vous n'avez pas encore de compte admin :
```bash
python manage.py createsuperuser
```

Suivez les instructions pour créer votre compte.

### Étape 4 : Donner les droits staff à un utilisateur existant
Si vous voulez qu'un utilisateur existant puisse modérer :

```bash
python manage.py shell
```

```python
from immo2app.models import Utilisateur

# Remplacez 'nom_utilisateur' par le nom d'utilisateur réel
user = Utilisateur.objects.get(username='nom_utilisateur')
user.is_staff = True
user.save()

exit()
```

---

## 📋 Utilisation

### Pour les utilisateurs normaux :
1. Connectez-vous
2. Cliquez sur "Ajouter un Bien"
3. Remplissez le formulaire et soumettez
4. **Nouveau** : Vous verrez un message "Bien ajouté avec succès ! Il sera publié après validation par un administrateur."
5. Le terrain n'apparaîtra PAS immédiatement sur le site
6. Il faut attendre qu'un administrateur le valide

### Pour les administrateurs :
1. Connectez-vous avec un compte administrateur (is_staff = True)
2. Un lien "⚙️ Modération" apparaît dans la barre de navigation
3. Cliquez dessus pour accéder au panneau de modération
4. Vous verrez 3 onglets :
   - **En attente** : Tous les terrains à valider
   - **Validés** : Les 10 derniers terrains validés
   - **Rejetés** : Les 10 derniers terrains rejetés
5. Pour chaque terrain en attente :
   - Visualisez toutes les informations (titre, prix, localisation, description, images)
   - Cliquez sur "✓ Valider" pour approuver → Le terrain devient visible sur le site
   - Cliquez sur "✗ Rejeter" pour refuser → Le terrain reste invisible

---

## 🎨 Personnalisation

### Modifier les couleurs du panneau de modération
Éditez le fichier `/immo2app/templates/moderation.html` dans la section `<style>`.

### Changer le message après ajout
Éditez le fichier `/immo2app/views.py`, ligne 72 :
```python
messages.success(request, "Votre message personnalisé ici")
```

---

## 📁 Fichiers modifiés

1. **models.py** - Ajout du champ `statut` au modèle Terrain
2. **views.py** - Ajout de 3 nouvelles vues (moderation, valider, rejeter) + modification des vues existantes
3. **urls.py** - Ajout des URLs de modération
4. **templates/navigation.html** - Ajout du lien Modération pour les admins
5. **templates/moderation.html** - Nouvelle page de modération (créée)
6. **migrations/0002_terrain_statut.py** - Migration pour ajouter le champ statut (créée)

---

## ⚠️ Important

- **Seuls les administrateurs** (utilisateurs avec `is_staff = True`) peuvent accéder au panneau de modération
- Les utilisateurs normaux verront une page de connexion s'ils tentent d'accéder à `/admin/moderation/`
- Les terrains en attente ou rejetés **ne sont jamais visibles** sur le site public
- Seuls les terrains avec `statut = 'valide'` apparaissent

---

## 🔧 Dépannage

### Le lien "Modération" n'apparaît pas
→ Vérifiez que votre utilisateur a `is_staff = True`

### "Permission denied" sur /admin/moderation/
→ Votre utilisateur doit avoir `is_staff = True`

### Les terrains validés n'apparaissent pas
→ Vérifiez que le statut est bien 'valide' (pas 'validé' ou autre variante)

### Erreur lors de la migration
→ Vérifiez que le nom de la dernière migration dans `0002_terrain_statut.py` correspond à votre dernier fichier de migration

---

## 📞 Support

Pour toute question, consultez la documentation Django : https://docs.djangoproject.com/

Bon courage ! 🚀
