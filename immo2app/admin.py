from django.contrib import admin
from .models import ImageTerrain, Terrain, Utilisateur
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


@admin.register(Terrain)
class TerrainAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_bien', 'statut_badge', 'prix', 'localisation', 'proprietaire', 'date_ajout']
    list_filter = ['statut', 'type_bien', 'date_ajout', 'localisation']
    search_fields = ['titre', 'localisation', 'description', 'proprietaire__username']
    readonly_fields = ['date_ajout']
    inlines = [ImageTerrainInline]
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('titre', 'type_bien', 'statut')
        }),
        ('Détails du bien', {
            'fields': ('superficie', 'prix', 'localisation', 'description')
        }),
        ('Propriétaire et date', {
            'fields': ('proprietaire', 'date_ajout')
        }),
    )
    
    def statut_badge(self, obj):
        colors = {
            'en_attente': '#ffc107',
            'valide': '#28a745',
            'rejete': '#dc3545'
        }
        icons = {
            'en_attente': '⏳',
            'valide': '✅',
            'rejete': '❌'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 10px; border-radius: 5px;">{} {}</span>',
            colors.get(obj.statut, '#6c757d'),
            icons.get(obj.statut, ''),
            obj.get_statut_display()
        )
    statut_badge.short_description = 'Statut'
    
    actions = ['valider_terrains', 'rejeter_terrains']
    
    def valider_terrains(self, request, queryset):
        count = queryset.update(statut='valide')
        self.message_user(request, f'{count} terrain(s) validé(s) avec succès.')
    valider_terrains.short_description = "✅ Valider les terrains sélectionnés"
    
    def rejeter_terrains(self, request, queryset):
        count = queryset.update(statut='rejete')
        self.message_user(request, f'{count} terrain(s) rejeté(s).')
    rejeter_terrains.short_description = "❌ Rejeter les terrains sélectionnés"


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

