from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.utils import timezone

# Create your models here.
def validate_keyword(value):
    keywords=[kw.strip() for kw in value.split(",") if kw.strip()]
    if len(keywords) > 10:
        raise ValidationError(
            f"Vous ne pouvez pas avoir plus de 10 mots-clés (actuellement {len(keywords)})."
        )
    
import uuid

def generate_submission_id():
    return "SUB" + uuid.uuid4().hex[:8].upper()


class Conference(models.Model):
    conference_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    description=models.TextField(validators=[MinLengthValidator(limit_value=30,message="la description doit contenir au minimum 30 caracteres")])
    location=models.CharField(max_length=255)
    THEME=[
        ("CS & IA","computer science & IA"),
        ("CS","Social Science"),
        ("SE","Science and Eng")
    ]
    theme=models.CharField(max_length=255,choices=THEME)
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        if self.start_date > self.end_date :
            raise ValidationError("la date de début de la conference doit etre inférieur à la fin")




class Submission(models.Model):
    id_submission=models.CharField(primary_key=True,unique=True,max_length=255,default=generate_submission_id,editable=False)
    user=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="submissions")
    conference=models.ForeignKey(Conference,on_delete=models.CASCADE,related_name="submissions")
    title=models.CharField(max_length=255)
    absract=models.TextField()
    keywords=models.TextField(validators=[validate_keyword])
    paper = models.FileField(
    upload_to="papers/",
    validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
)
    STATUS=[
        ("submitted","submitted"),
        ("under_review","under review"),
        ("rejected","rejected")
    ]
    status=models.CharField(max_length=255,choices=STATUS)
    payed=models.BooleanField(default=False)
    submission_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def clean(self):
        today = timezone.localdate()
        if self.conference.start_date <= today:
            raise ValidationError("Vous ne pouvez soumettre que pour une conférence à venir.")

        submissions_today = Submission.objects.filter(
            user=self.user,
            submission_date=today
        ).count()

        if submissions_today >= 3:
            raise ValidationError("Vous avez déjà atteint la limite de 3 soumissions pour aujourd'hui.")


