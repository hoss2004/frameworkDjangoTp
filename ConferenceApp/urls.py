from django.urls import path
#from . import views
from .views import ConferenceList,ConferenceDetails,ConferenceCreate,ConferenceUpdate,ConferenceDelete
urlpatterns=[
    #path("liste/",views.all_conferences,name="conference_liste")
    path("liste/",ConferenceList.as_view(),name="conference_liste"),
     path("details/<int:pk>/", ConferenceDetails.as_view(), name="ConferenceDetails"),
     path("form/", ConferenceCreate.as_view(), name="conference_add"),
     path("<int:pk>/edit/", ConferenceUpdate.as_view(), name="conference_edit"),
     path("<int:pk>/delete/", ConferenceDelete.as_view(), name="conference_delete"),
]
