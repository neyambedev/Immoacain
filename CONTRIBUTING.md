# 🤝 Guide de Contribution

Merci de votre intérêt pour contribuer à ACAIN Immobilier ! Voici comment vous pouvez aider.

## 📋 Code de Conduite

- Soyez respectueux et professionnel
- Acceptez les critiques constructives
- Concentrez-vous sur ce qui est meilleur pour la communauté

## 🚀 Comment Contribuer

### 1. Signaler un Bug

Avant de créer une issue :
- Vérifiez qu'elle n'existe pas déjà
- Utilisez le template d'issue si disponible

Incluez :
- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs actuel
- Captures d'écran si pertinent
- Environnement (OS, navigateur, version Django)

### 2. Proposer une Fonctionnalité

- Ouvrez une issue avec le tag `enhancement`
- Décrivez clairement la fonctionnalité
- Expliquez pourquoi elle serait utile
- Proposez une implémentation si possible

### 3. Soumettre du Code

#### Fork & Clone
```bash
# Fork le projet sur GitHub
# Puis clonez votre fork
git clone https://github.com/VOTRE_USERNAME/immo2.git
cd immo2
```

#### Créer une Branche
```bash
git checkout -b feature/nom-de-la-fonctionnalite
# ou
git checkout -b fix/nom-du-bug
```

#### Développer

1. **Suivez les conventions de code Django**
2. **Écrivez des tests** pour votre code
3. **Commentez** le code complexe
4. **Respectez PEP 8** (style Python)

#### Tester
```bash
python manage.py test
python manage.py runserver
# Testez manuellement
```

#### Commiter
```bash
git add .
git commit -m "feat: ajouter recherche avancée par prix"
```

**Format des commits :**
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `style:` Formatage (sans changement de code)
- `refactor:` Refactorisation
- `test:` Ajout de tests
- `chore:` Tâches diverses

#### Pousser & Pull Request
```bash
git push origin feature/nom-de-la-fonctionnalite
```

Puis sur GitHub :
1. Créez une Pull Request
2. Décrivez vos changements
3. Liez les issues concernées
4. Attendez la review

## 📝 Standards de Code

### Python/Django
```python
# Bon
def get_terrains_by_location(location):
    """Récupère les terrains par localisation."""
    return Terrain.objects.filter(localisation__icontains=location)

# Mauvais
def get_t(l):
    return Terrain.objects.filter(localisation__icontains=l)
```

### HTML/Templates
```html
<!-- Bon : Indenté, commenté -->
{% extends "base.html" %}

{% block content %}
    <div class="container">
        <!-- Liste des terrains -->
        {% for terrain in terrains %}
            ...
        {% endfor %}
    </div>
{% endblock %}
```

### CSS
```css
/* Bon : Noms clairs, organisation */
.terrain-card {
    background: white;
    border-radius: 12px;
}

/* Mauvais */
.tc { background: #fff; border-radius: 12px; }
```

## ✅ Checklist avant Pull Request

- [ ] Code fonctionne localement
- [ ] Tests passent
- [ ] Code suit les conventions Django/PEP 8
- [ ] Documentation mise à jour si nécessaire
- [ ] Pas de fichiers sensibles (.env, db.sqlite3)
- [ ] Commit messages clairs
- [ ] Pull Request décrit les changements

## 🎯 Priorités de Contribution

### Hautement recherché
- Amélioration des performances
- Correction de bugs critiques
- Tests unitaires
- Documentation

### Recherché
- Nouvelles fonctionnalités
- Amélioration UI/UX
- Traductions
- Exemples d'utilisation

### Appréciable
- Optimisations
- Refactoring
- Commentaires de code

## 🐛 Déboggage

### Activer le mode debug
```python
# settings.py
DEBUG = True
ALLOWED_HOSTS = ['*']
```

### Voir les logs
```bash
python manage.py runserver --noreload
```

### Shell Django
```bash
python manage.py shell
>>> from immo2app.models import Terrain
>>> Terrain.objects.all()
```

## 📚 Ressources

- [Django Documentation](https://docs.djangoproject.com/)
- [PEP 8](https://pep8.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)

## 💬 Questions ?

- Ouvrez une issue avec le tag `question`
- Contactez les mainteneurs
- Consultez la documentation

## 🙏 Merci !

Chaque contribution, petite ou grande, est appréciée et aide à améliorer le projet.

---

**Happy Coding!** 💻✨
