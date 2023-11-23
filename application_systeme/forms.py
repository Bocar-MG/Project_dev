from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Offre, Cv


class UserForm(UserCreationForm):
    ROLE_CHOICES = (
        ('admin', 'recruteur'),
        ('user', 'candidat'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rôle')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'


        ]

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        if self.cleaned_data['role'] == 'admin':
            user.is_superuser = True
        if commit:
            user.save()
        return user



class OffreForm(forms.ModelForm):
    class Meta:
        model = Offre
        fields = ['titre', 'experience', 'competence', 'formation', 'description','image','publication','date_limite']


class CvForm(forms.ModelForm):
    class Meta:
        model = Cv
        fields = ['cv_file', 'lettre']