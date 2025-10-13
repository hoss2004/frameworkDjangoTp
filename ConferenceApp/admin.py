# ConferenceApp/admin.py
from django.contrib import admin
from .models import Conference, Submission

# --------- Personnalisation globale du site admin ---------
admin.site.site_header = "Conference Management Admin 25/26"
admin.site.site_title = "Conference Dashboard"
admin.site.index_title = "conference management"


# =========================
# Inlines pour Submission
# =========================

# Variante empilée (verticale)
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 0
    show_change_link = True
    fields = (
        "id_submission",    # lecture seule
        "title",
        "absract",          # ⚠️ selon ton modèle
        "status",
        "payed",            # ⚠️ 'paid' si renommé
        "user",
        "submission_date",  # lecture seule
    )
    readonly_fields = ("id_submission", "submission_date")


# Variante tabulaire (tableau compact)
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 0
    show_change_link = True
    fields = ("title", "status", "user", "payed")  # colonnes principales
    readonly_fields = ()  # rien en RO dans la version tableau


# =========================
# Admin Conference
# =========================
@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    # a + c : colonnes + durée
    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")

    # d : filtres
    list_filter = ("theme", "location", "start_date")

    # e : recherche
    search_fields = ("name", "description", "location")

    # f : fieldsets
    fieldsets = (
        ("Informations générales", {"fields": ("name", "theme", "description")}),
        ("Logistique", {"fields": ("location", "start_date", "end_date")}),
    )

    # g : ordering
    ordering = ("start_date",)

    # h : navigation par calendrier
    date_hierarchy = "start_date"

    # Inline à utiliser (choisis l’un des deux)
    inlines = [SubmissionTabularInline]
    # inlines = [SubmissionStackedInline]

    # b : méthode durée (jours inclusifs)
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days + 1
        return "-"
    duration.short_description = "Durée (jours)"
    duration.admin_order_field = "start_date"


# =========================
# Admin Submission
# =========================
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    # a + c : colonnes + méthode short_abstract
    list_display = (
        "title",
        "short_abstract",
        "status",
        "payed",            # ⚠️ 'paid' si renommé
        "user",
        "conference",
        "submission_date",
    )
    list_display_links = ("title",)

    # f : édition directe depuis la liste
    list_editable = ("status", "payed")

    # d : filtres
    list_filter = ("status", "payed", "conference", "submission_date")

    # e : recherche
    search_fields = ("title", "keywords", "user__username")

    # g : fieldsets du formulaire
    fieldsets = (
        ("Infos générales", {"fields": ("id_submission", "title", "absract", "keywords")}),
        ("Fichier et conférence", {"fields": ("paper", "conference")}),
        ("Suivi", {"fields": ("status", "payed", "submission_date", "user")}),
    )

    # h : lecture seule
    readonly_fields = ("id_submission", "submission_date")

    # b : résumé tronqué à 50 caractères
    def short_abstract(self, obj):
        text = getattr(obj, "absract", "") or ""  # 'absract' selon ton modèle
        return (text[:47] + "…") if len(text) > 50 else text
    short_abstract.short_description = "Résumé (50c)"
