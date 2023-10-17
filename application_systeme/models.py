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


