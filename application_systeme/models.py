from django.db import models

# Create your models here.

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Offre(models.Model):
    titre = models.CharField(max_length=100)
    Nom_societe = models.CharField(max_length=100,null=True)
    experience = models.CharField(max_length=100)
    competence = models.CharField(max_length=100)
    formation = models.CharField(max_length=100)
    description = models.TextField()
    publication = models.BooleanField(default=False)
    date_limite = models.DateField(default=timezone.now)
    image = models.ImageField(default='icon_about.png',upload_to='uploaded_images/')
    recruteur = models.ForeignKey(User,on_delete=models.CASCADE)


class Cv(models.Model):
    candidat = models.ForeignKey(User,on_delete=models.CASCADE)
    nom_user= models.CharField(max_length=50)
    email_user=models.EmailField()
    cv_file=models.FileField(upload_to='cvs')
    lettre=models.TextField()
    numero_offre = models.ForeignKey(Offre,on_delete=models.CASCADE, null=True)
    Etat = models.BooleanField(null=True,default=False)


class Postulation(models.Model):
    societe = models.CharField(max_length=50)
    Poste = models.CharField(max_length=50)
    date_postuler = models.CharField(max_length=50,null=True)
    Etat = models.CharField(max_length=50,default="En cours")
    numero_offre = models.IntegerField(null=True)