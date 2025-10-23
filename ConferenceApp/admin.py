# ConferenceApp/admin.py
from django.contrib import admin
from .models import Conference, Submission
admin.site.site_header = "Conference Management Admin 25/26"
admin.site.site_title = "Conference Dashboard"
admin.site.index_title = "conference management"
class SubmissionStackedInline(admin.StackedInline):
    model = Submission
    extra = 0
    show_change_link = True
    fields = (
        "id_submission",    
        "title",
        "absract",          
        "status",
        "payed",            
        "user",
        "submission_date",  
    )
    readonly_fields = ("id_submission", "submission_date")


# Variante tabulaire (tableau compact)
class SubmissionTabularInline(admin.TabularInline):
    model = Submission
    extra = 0
    show_change_link = True
    fields = ("title", "status", "user", "payed") 
    readonly_fields = ()  


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):

    list_display = ("name", "theme", "location", "start_date", "end_date", "duration")

    list_filter = ("theme", "location", "start_date")

    search_fields = ("name", "description", "location")

    fieldsets = (
        ("Informations générales", {"fields": ("name", "theme", "description")}),
        ("Logistique", {"fields": ("location", "start_date", "end_date")}),
    )

    ordering = ("start_date",)
    date_hierarchy = "start_date"
    inlines = [SubmissionTabularInline]
    def duration(self, obj):
        if obj.start_date and obj.end_date:
            return (obj.end_date - obj.start_date).days + 1
        return "-"
    duration.short_description = "Durée (jours)"
    duration.admin_order_field = "start_date"

@admin.action(description="marqué commme payé")
def mark_as_payed(modeladmin,req,queryset):
    queryset.update(payed=True)
@admin.action
def mark_as_accepted(m,req,q):
    q.update(status="submitted")

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    
    list_display = (
        "title",
        "short_abstract",
        "status",
        "payed",           
        "user",
        "conference",
        "submission_date",
    )
    actions=[mark_as_payed,mark_as_accepted]
    list_display_links = ("title",)

   
    list_editable = ("status", "payed")

    list_filter = ("status", "payed", "conference", "submission_date")

 
    search_fields = ("title", "keywords", "user__username")


    fieldsets = (
        ("Infos générales", {"fields": ("id_submission", "title", "absract", "keywords")}),
        ("Fichier et conférence", {"fields": ("paper", "conference")}),
        ("Suivi", {"fields": ("status", "payed", "submission_date", "user")}),
    )

   
    readonly_fields = ("id_submission", "submission_date")

  
    def short_abstract(self, obj):
        text = getattr(obj, "absract", "") or "" 
        return (text[:47] + "…") if len(text) > 50 else text
    short_abstract.short_description = "Résumé (50c)"
