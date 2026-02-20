# 🏠 ACAIN Immobilier - Site Web Django

Site web immobilier moderne pour la gestion et l'affichage de biens immobiliers (terrains, maisons, locations).

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

## 📋 Description

ACAIN Immobilier est une plateforme web permettant de :
- 📍 Publier et gérer des biens immobiliers (terrains, maisons, locations)
- 🔍 Rechercher des biens par quartier
- 📸 Afficher des galeries d'images avec carrousel
- 👤 Gérer les utilisateurs et propriétaires
- 🎨 Interface moderne et responsive

## ✨ Fonctionnalités

### Pour les Visiteurs
- ✅ Navigation par type de bien (Terrains, Maisons, Locations)
- ✅ Recherche par localisation
- ✅ Galerie d'images avec carrousel
- ✅ Interface responsive (mobile/tablette/desktop)
- ✅ Design moderne avec badges colorés

### Pour les Utilisateurs Connectés
- ✅ Ajout de nouveaux biens
- ✅ Upload multiple d'images (drag & drop)
- ✅ Gestion de leurs annonces
- ✅ Profil personnalisé

### Pour les Administrateurs
- ✅ Interface d'administration Django complète
- ✅ Gestion des utilisateurs
- ✅ Modération des annonces
- ✅ Statistiques

## 🛠️ Technologies Utilisées

- **Backend :** Django 5.0
- **Frontend :** Bootstrap 5.3, HTML5, CSS3
- **Base de données :** SQLite (dev) / PostgreSQL (production)
- **JavaScript :** Vanilla JS, AJAX
- **Icônes :** Bootstrap Icons

## 📦 Installation

### Prérequis
- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Git

### Étapes d'installation

1. **Cloner le repository**
```bash
git clone https://github.com/VOTRE_USERNAME/immo2.git
cd immo2
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Créer le fichier .env** (voir section Configuration)
```bash
cp .env.example .env
# Éditer .env avec vos valeurs
```

5. **Effectuer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

7. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic --no-input
```

8. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

9. **Accéder au site**
- Site : http://127.0.0.1:8000
- Admin : http://127.0.0.1:8000/admin

## ⚙️ Configuration

### Fichier .env

Créez un fichier `.env` à la racine du projet :

```env
# Django
SECRET_KEY=votre-clé-secrète-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DATABASE_URL=sqlite:///db.sqlite3

# Email (optionnel)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=votre@email.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe
```

### Générer une SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 📁 Structure du Projet

```
immo2/
├── immo2/                      # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── immo2app/                   # Application principale
│   ├── models.py               # Modèles (Utilisateur, Terrain, ImageTerrain)
│   ├── views.py                # Vues
│   ├── forms.py                # Formulaires
│   ├── admin.py                # Configuration admin
│   ├── middleware.py           # Middleware personnalisé
│   ├── templates/              # Templates HTML
│   │   ├── base.html
│   │   ├── navigation.html
│   │   ├── home.html
│   │   ├── liste_terrains.html
│   │   └── ...
│   └── static/                 # Fichiers statiques
│       └── immo2app/
│           ├── css/
│           │   └── style-moderne.css
│           ├── js/
│           └── images/
├── media/                      # Fichiers uploadés
├── .gitignore
├── requirements.txt
├── README.md
└── manage.py
```

## 🎨 Personnalisation

### Modifier les couleurs
Éditez `immo2app/static/immo2app/css/style-moderne.css` :

```css
:root {
    --primary: #2563eb;      /* Bleu principal */
    --secondary: #10b981;    /* Vert */
    --accent: #f59e0b;       /* Orange */
}
```

### Modifier le logo
Remplacez `immo2app/static/images/logo.jpg`

## 🚀 Déploiement

### Heroku

```bash
# Installer Heroku CLI
heroku create nom-de-votre-app
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### PythonAnywhere

1. Créer un compte sur PythonAnywhere
2. Cloner votre repository
3. Créer un environnement virtuel
4. Configurer le fichier WSGI
5. Recharger l'application

## 📝 Utilisation

### Ajouter un bien

1. Connectez-vous
2. Cliquez sur "Ajouter"
3. Remplissez le formulaire
4. Uploadez des images (drag & drop supporté)
5. Cliquez sur "Enregistrer"

### Rechercher un bien

1. Utilisez la barre de recherche en haut
2. Tapez le nom d'un quartier
3. Les résultats s'affichent en temps réel

## 🤝 Contribution

Les contributions sont les bienvenues !

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Poussez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👨‍💻 Auteur

**Votre Nom**
- GitHub: [@votre-username](https://github.com/votre-username)
- Email: votre@email.com

## 🙏 Remerciements

- Django Documentation
- Bootstrap Team
- Bootstrap Icons
- Communauté open source

## 📞 Support

Pour toute question ou problème :
- Ouvrez une [issue](https://github.com/votre-username/immo2/issues)
- Envoyez un email à support@acain-immo.com

---

**Fait avec ❤️ pour faciliter la gestion immobilière**
