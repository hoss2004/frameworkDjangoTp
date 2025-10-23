from django.shortcuts import render
from .models import Conference
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ConferenceModel

def all_conferences(req):
    conference_liste=Conference.objects.all()
    return render(req,'Conference/liste.html',{"liste":conference_liste})

class ConferenceList(ListView):
    model=Conference
    context_object_name= "liste"
    ordering=['start_date']
    template_name="Conference/liste.html"

class ConferenceDetails(DetailView):
    model = Conference
    queryset = Conference.objects.all()
    context_object_name = "conference"
    template_name = "Conference/ConferenceDetails.html"
    pk_url_kwarg = "pk"                     

# Create your views here.
class ConferenceCreate(CreateView):
    model=Conference
    template_name="conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel

    success_url=reverse_lazy("conference_liste")

class ConferenceUpdate(UpdateView):
    model=Conference
    template_name="conference/conference_form.html"
    #fields="__all__"
    form_class=ConferenceModel
    success_url=reverse_lazy("conference_liste")

class ConferenceDelete(DeleteView):
    model=Conference
    template_name="conference/conference_confirm_delete.html"
    success_url=reverse_lazy("conference_liste")

    
    