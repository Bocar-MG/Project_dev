import datetime
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import spacy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from spacy.matcher import Matcher

from application_systeme.convert_pdf_to_txt import pdf_to_text
from application_systeme.forms import UserForm, OffreForm, CvForm
from application_systeme.model_cv_training import competence_patterns, formation_patterns, experience_patterns, \
    certification_patterns, langages_patterns
from application_systeme.models import Offre, Postulation, Cv, Classement


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
    competences_matcher = []
    formations_matcher = []
    experiences_matcher = []
    certification_matcher = []
    langages = []
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

        # utiisation de la librairie SpaCy
        nlp = spacy.load('fr_core_news_sm')

        cv_filepdf = cv.cv_file
        with cv_filepdf.open() as f:
            with NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(f.read())
                file_path = Path(tmp_file.name)
           # tmp_file.close()
            #os.remove(tmp_file.name)

        texte_brute = pdf_to_text(file_path).lower()
        # print(texte_brute)
        print(texte_brute)
        doc = nlp(texte_brute)

        matcher = Matcher(nlp.vocab)
        matcher.add("COMPETENCE", competence_patterns)
        matcher.add("FORMATION", formation_patterns)
        matcher.add("EXPERIENCE", experience_patterns)
        matcher.add("CERTIFICATION", certification_patterns)
        matcher.add("LANGUE", langages_patterns)

        matches = matcher(doc)
        for match_id, start, end in matches:
            if nlp.vocab.strings[match_id] == "COMPETENCE":
                competences_matcher.append(doc[start:end].text)
            elif nlp.vocab.strings[match_id] == "FORMATION":
                formations_matcher.append(doc[start:end].text)
            elif nlp.vocab.strings[match_id] == "EXPERIENCE":
                experiences_matcher.append(doc[start:end].text)
            elif nlp.vocab.strings[match_id] == "CERTIFICATION":
                certification_matcher.append(doc[start:end].text)

        print(experiences_matcher)
        print(competences_matcher)
        print(formations_matcher)
        print(certification_matcher)
        print("###### Traitement des donneés extraite #######")
        competence_offre = str(offre.competence).split(',')
        comp_strip = []
        formation_offre = str(offre.formation).split(',')
        form_strip = []
        for comp in competence_offre:
            comp_strip.append(comp.strip())
        for form in formation_offre:
            form_strip.append(form)
        # Comptence extraction and compare
        print(comp_strip)
        print(form_strip)
        scoreCompétence = 0
        scoreFormation = 0
        for competence in comp_strip:
            if competence in set(competences_matcher):
                scoreCompétence = scoreCompétence + 10
                print(f"compétence trouvé: {competence}")
        print(f"votre candidature correspond a {scoreCompétence} %")

        for formation in form_strip:
            if formation in set(formations_matcher):
                scoreFormation = scoreFormation + 10
                print(f"Formation trouvé:{competence}")
        print(f"votre candidature correspond a {scoreFormation} %")
        total = scoreFormation + scoreCompétence
        # J'ai diviser le score en deux categorie formation et compétence si vous pouvez l'ameliorer
        # je modifie en meme le champs etat de la table cv du l'utilisateur
        if total >= 50:
            cv.Etat = True
        cv.save()
        print(cv.Etat)
        # Ici je remplie la tbale classement pour que le recruteur puisse voir, vous pouvez aussi l'ameliorer selon vos suggestions
        table = Classement.objects.create(NomCandidat=request.user.username, email_candidat=request.user.email,
                                          Titre_offre=offre.titre, Score=total, cv=cv)
        table.save()

        tmp_file.close()
        os.remove(tmp_file.name)


        competences_matcher.clear()
        formations_matcher.clear()
        experiences_matcher.clear()
        certification_matcher.clear()

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
        tableauClassement = Classement.objects.all()
        return render(request,'application_systeme/classement.html',{'tableauClassement':tableauClassement})

@login_required
def supprimerCandidat(request,id):
    if request.user.is_authenticated:
        candidat = Classement.objects.get(id=id)
        candidat.delete()
        return redirect('classement')