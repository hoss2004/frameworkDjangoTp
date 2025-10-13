from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
name_validator=RegexValidator(
    regex=r'^[A-Za-z0-9]+$',
    message="le nom de la salle ne doit contenir que des lettres et des chiffres"
)
# Create your models here.
class Session(models.Model):
    session_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    topic=models.CharField(max_length=255)
    session_day=models.DateField()
    start_time=models.DateTimeField()
    end_time=models.DateTimeField()
    room=models.CharField(max_length=255,validators=[name_validator])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="sessions")
    def clean(self):
        if self.conference:
            if not(self.conference.start_date<=self.session_day<=self.conference.end_date):
                raise ValidationError("la date de la session doit etre comprise entre les date de la conference")
            if self.end_time<=self.start_time:
                raise ValidationError("l heure doit de fin doit etre superieure a l heure de debut")
    