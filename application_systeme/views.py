import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from application_systeme.forms import UserForm, OffreForm, CvForm
from application_systeme.models import Offre, Postulation, Cv


# Create your views here.

@login_required
def pagerecruteur(request):
    return render(request, 'application_systeme/dashrecruteur.html')


def inscription(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
        else:
            messages.error(request, form.errors)
    return render(request, 'application_systeme/signup.html', {'form': form})


def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            if user.is_superuser:
                login(request, user)
                return redirect('stats')
            else:
                login(request, user)
                return redirect('user_interface')
        else:
            messages.error(request, "erreur d'authentification")
    return render(request, 'application_systeme/signin.html')


def index(request):
    offres = Offre.objects.filter(publication=True)
    val = "Postuler Maintenant"
    if request.user.is_authenticated & request.user.is_superuser:
        val = "Voir le detail"
    return render(request, 'application_systeme/index.html', {'offres': offres, 'val': val})


def lister_offres_index(request):
    offres = Offre.objects.filter(publication=True)
    val = "Postuler Maintenant"
    if request.user.is_superuser:
        val = "Voir le detail"

    return render(request, 'application_systeme/liste_job.html', {'offres': offres, 'val': val})


@login_required
def ajouter_offre(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = OffreForm(request.POST, request.FILES)
            if form.is_valid():
                offre = form.save(commit=False)
                offre.recruteur = request.user
                offre.Nom_societe = request.user.username
                offre.save()
                return redirect('listes')
        else:
            form = OffreForm()
        return render(request, 'application_systeme/ajouter_offre.html', {'form': form})


@login_required
def lister_offres(request):
    if request.user.is_authenticated:
        offres = Offre.objects.filter(recruteur_id=request.user)
        return render(request, 'application_systeme/listes_offres.html', {'offres': offres})


def UpdateOffre(request, id):
    offre = Offre.objects.get(id=id)
    if request.method == "POST":
        update_offre = OffreForm(request.POST, request.FILES, instance=offre)
        if update_offre.is_valid():
            update_offre.save()
            return redirect('listes')

    else:
        update_offre = OffreForm(instance=offre)
    return render(request, 'application_systeme/update_offre.html', {'update_offre': update_offre})


@login_required
def SupprimerOffre(request, id):
    offre = Offre.objects.get(id=id)
    offre.delete()
    return redirect('listes')


@login_required
def Deconnexion(request):
    logout(request)
    return redirect('index')


@login_required
def Stats(request):
    cv_all = []
    if request.user.is_authenticated:
        offres = Offre.objects.filter(recruteur_id=request.user)
        cvs = Cv.objects.all()
        for offre in offres:
            for cv in cvs:
                if (cv.numero_offre == offre):
                    cv_all.append(cv)
            #  cv.append(Cv.objects.filter(numero_offre_id = offre.id))

        nbres_offres = len(offres)

        nbr_candidats = len(cv_all)
        print(nbres_offres)
        return render(request, 'application_systeme/dashrecruteur.html',
                          {'nbres_offres': nbres_offres, 'nbr_candidats': nbr_candidats})


@login_required
def interface_user(request):
    if request.user.is_authenticated:
        user = request.user
        cvs = Cv.objects.filter(candidat=user)
        return render(request,'application_systeme/dashcandidats.html',{'cvs':cvs})


@login_required
def offre_detail(request, id):
    user = request.user
    offre = Offre.objects.get(id=id)
    form = CvForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        cv = form.save(commit=False)
        cv.candidat = request.user
        cv.nom_user = request.user.username
        cv.email_user = request.user.email
        cv.numero_offre = offre
        cv.save()
        messages.success(request, 'Votre candidature a été envoyée avec succès')

        ####### Traitement Pour NLP ########


        ####### Traitement Pour NLP ########

        return redirect('user_interface')
    context = {'form': form, 'offre': offre, 'user': user}
    return render(request, 'application_systeme/offre_detail.html', context)

@login_required
def postuler(request,id):
    if request.user.is_authenticated:
        # Tes donnes du post ici normalement
        offre_postuler = Offre.objects.get(id=id)
        candidature = Postulation.objects.create(Nom_societe=offre_postuler.Nom_societe,Poste=offre_postuler.titre,date_postuler=datetime.datetime.now,numero_offre=id)
        candidature.save()
        redirect('user_interface')


@login_required
def classementListe(request):
    if request.user.is_authenticated:

        return render(request,'application_systeme/classement.html')