from django import forms
from .models import Conference
class ConferenceModel(forms.ModelForm):
    class Meta:
        model=Conference
        fields=['name','theme','description','location','start_date','end_date']
        labels={
            'name':"nom de la conférence",
            'theme':"thématiques",
            'description':"Description",
            'location':"Location",
            'start_date':"date début de la conférence",
            'end_date':"date fin de la conférence",

        }
        widgets={
            'start_date': forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de début",

                }
            ),
            'end_date': 
            forms.DateInput(
                attrs={
                    'type':'date',
                    'placeholder':"date de fin",

                }
            ),
            'name':forms.TextInput(
                attrs={
                    'placeholder':"Ex - Conference IA"
                }
            ),
        }

