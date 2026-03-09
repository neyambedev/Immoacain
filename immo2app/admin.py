from django.contrib import admin
from .models import ImageTerrain, VideoTerrain, Terrain, Utilisateur
from django.utils.html import format_html


@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'Telephone', 'ville', 'is_staff']
    list_filter = ['is_staff', 'is_active', 'ville']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'Telephone']


class ImageTerrainInline(admin.TabularInline):
    model = ImageTerrain
    extra = 1
    fields = ['image', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'


class VideoTerrainInline(admin.TabularInline):
    model = VideoTerrain
    extra = 1
    fields = ['video', 'video_preview']
    readonly_fields = ['video_preview']

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video src="{}" style="max-height: 100px; max-width: 150px;" controls muted preload="metadata"></video>',
                obj.video.url
            )
        return "Pas de vidéo"
    video_preview.short_description = 'Aperçu vidéo'


@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_bien', 'statut_badge', 'disponibilite_badge', 'reservation_badge', 'prix', 'localisation', 'proprietaire', 'date_ajout']
    list_filter = ['statut', 'type_bien', 'disponible', 'reservee', 'date_ajout', 'localisation']
    search_fields = ['titre', 'localisation', 'description', 'proprietaire__username']
    readonly_fields = ['date_ajout']
    inlines = [ImageTerrainInline, VideoTerrainInline]

    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'type_bien', 'statut')
        }),
        ('Disponibilité', {
            'fields': ('disponible', 'reservee'),
            'description': 'Contrôlez la visibilité du bien sur le marché.',
        }),
        ('Détails du bien', {
            'fields': ('superficie', 'prix', 'localisation', 'quartier', 'description')
        }),
        ('Location', {
            'fields': ('nom_location', 'categorie_location', 'duree_location'),
            'classes': ('collapse',),
        }),
        ('Propriétaire et date', {
            'fields': ('proprietaire', 'date_ajout')
        }),
    )

    def statut_badge(self, obj):
        colors = {'en_attente': '#ffc107', 'valide': '#28a745', 'rejete': '#dc3545'}
        icons  = {'en_attente': '⏳', 'valide': '✅', 'rejete': '❌'}
        return format_html(
            '<span style="background:{};color:white;padding:4px 10px;border-radius:5px;">{} {}</span>',
            colors.get(obj.statut, '#6c757d'), icons.get(obj.statut, ''), obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'

    def disponibilite_badge(self, obj):
        if obj.disponible:
            return format_html('<span style="background:#00b894;color:white;padding:4px 10px;border-radius:5px;">👁 Visible</span>')
        return format_html('<span style="background:#636e72;color:white;padding:4px 10px;border-radius:5px;">🚫 Masqué</span>')
    disponibilite_badge.short_description = 'Marché'

    def reservation_badge(self, obj):
        if obj.categorie_location != 'hotel':
            return format_html('<span style="color:#ccc;">—</span>')
        if obj.reservee:
            return format_html('<span style="background:#e17055;color:white;padding:4px 10px;border-radius:5px;">🔒 Réservée</span>')
        return format_html('<span style="background:#0984e3;color:white;padding:4px 10px;border-radius:5px;">🟢 Libre</span>')
    reservation_badge.short_description = 'Réservation'

    actions = ['valider_terrains', 'rejeter_terrains', 'rendre_disponible', 'masquer_marche', 'marquer_reservee', 'liberer_chambre']

    def valider_terrains(self, request, queryset):
        count = queryset.update(statut='valide')
        self.message_user(request, f'{count} bien(s) validé(s).')
    valider_terrains.short_description = "✅ Valider les biens sélectionnés"

    def rejeter_terrains(self, request, queryset):
        count = queryset.update(statut='rejete')
        self.message_user(request, f'{count} bien(s) rejeté(s).')
    rejeter_terrains.short_description = "❌ Rejeter les biens sélectionnés"

    def rendre_disponible(self, request, queryset):
        count = queryset.update(disponible=True)
        self.message_user(request, f'{count} bien(s) remis sur le marché.')
    rendre_disponible.short_description = "👁 Rendre disponible (visible sur le marché)"

    def masquer_marche(self, request, queryset):
        count = queryset.update(disponible=False)
        self.message_user(request, f'{count} bien(s) masqué(s) du marché.')
    masquer_marche.short_description = "🚫 Masquer du marché"

    def marquer_reservee(self, request, queryset):
        hotels = queryset.filter(categorie_location='hotel')
        count = hotels.update(reservee=True, disponible=False)
        self.message_user(request, f'{count} chambre(s) marquée(s) comme réservée(s).')
    marquer_reservee.short_description = "🔒 Marquer chambre(s) hôtel comme réservée(s)"

    def liberer_chambre(self, request, queryset):
        hotels = queryset.filter(categorie_location='hotel')
        count = hotels.update(reservee=False, disponible=True)
        self.message_user(request, f'{count} chambre(s) libérée(s) et remise(s) sur le marché.')
    liberer_chambre.short_description = "🟢 Libérer chambre(s) hôtel (remettre disponible)"


@admin.register(ImageTerrain)
class ImageTerrainAdmin(admin.ModelAdmin):
    list_display = ['terrain', 'image_preview']
    list_filter = ['terrain__type_bien']
    search_fields = ['terrain__titre']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px;" />', obj.image.url)
        return "Pas d'image"
    image_preview.short_description = 'Aperçu'


@admin.register(VideoTerrain)
class VideoTerrainAdmin(admin.ModelAdmin):
    list_display = ['terrain', 'video_preview']
    list_filter = ['terrain__type_bien']
    search_fields = ['terrain__titre']

    def video_preview(self, obj):
        if obj.video:
            return format_html(
                '<video src="{}" style="max-height: 100px; max-width: 180px;" controls muted preload="metadata"></video>',
                obj.video.url
            )
        return "Pas de vidéo"
    video_preview.short_description = 'Aperçu vidéo'

