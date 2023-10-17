from django.urls import path, include
from .views import inscription, connexion, ajouter_offre, lister_offres, pagerecruteur, Deconnexion, UpdateOffre, \
    SupprimerOffre, index, lister_offres_index, Stats, offre_detail, interface_user

urlpatterns = [

    path('', index, name='index'),
    path('signup/', inscription, name='signup'),
    path('login/', connexion, name='signin'),
    path('offre/', ajouter_offre, name='interface_offre'),
    path('user_simple/', interface_user, name='user_interface'),
    path('listes/', lister_offres, name='listes'),
    path('statistiques/', Stats, name='stats'),
    path('detail/<int:id>', offre_detail, name='offre_detail'),
    path('listes_index/', lister_offres_index, name='listes_index'),
    path('dashrecruteur/', pagerecruteur, name='recruteurdash'),
    path('logout/', Deconnexion, name='Deconnexion'),
    path('update/<int:id>', UpdateOffre, name='update_offre'),
    path('delete/<int:id>', SupprimerOffre, name='suppression'),

]
