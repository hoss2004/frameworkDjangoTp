from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# Create your models here.
import uuid #bibliotheque qui genere des listes des caracteres ou des lettres
def generate_userid():
    return "USER"+uuid.uuid4().hex[:4].upper()

def verify_email(email):
    domaine=["esprit.tn","seasame.com","tekup.tn","central.com"]
    if email.split("@")[1] not in domaine:
        raise ValidationError("l email est invalkde et dout appartenir a un demaine unversaire")
    
name_validator=RegexValidator(
    regex= r'^[A-Za-z\s-]+$',
    message="le champ doit avoir des lettres et des espaces"

)

class User(AbstractUser):
    user_id=models.CharField(max_length=8,primary_key=True,unique=True,editable=False)
    first_name=models.CharField(max_length=100,validators=[name_validator])
    last_name=models.CharField(max_length=100,validators=[name_validator])
    email=models.EmailField(unique=True, validators=[verify_email])
    affiliation=models.CharField(max_length=255)
    nationality=models.CharField(max_length=255)
    ROLE=[
        ("participant","Participant"),
        ("commitee","orgonizing commitee member")
    ]
    role=models.CharField(max_length=255,choices=ROLE,default="participant")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def save(self,*args,**kwargs):#fonctoin predifinie pour ajouter le user dans la base de donnée
        if not self.user_id:
            new_id=generate_userid()
            while User.objects.filter(user_id=new_id).exists():
                new_id=generate_userid()
            self.user_id=new_id
        super().save(*args,**kwargs)


    #submissions=models.ManyToManyField("ConferenceApp.Conference",through="Submisson") ken theb tistaamelhom , fasakh related name fel organizing commitee w submission
    #Organizing_CommiteeList=models.ManyToManyField("ConferenceApp.Conference",through="Organizing_Commitee")


class Organizing_Commitee(models.Model):
    user=models.ForeignKey("UserApp.User",on_delete=models.CASCADE,related_name="commitee")
    conference=models.ForeignKey("ConferenceApp.Conference",on_delete=models.CASCADE,related_name="commitee")
    ROLES=[
        ("chair","chair"),
        ("co-chair","co-chair"),
        ("member","member"),
    ]
    commitee_role=models.CharField(max_length=255,choices=ROLES)
    date_joined=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    
