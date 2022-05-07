from django.urls import include, path
from . import views
from .views import ProposalList, ProposalUpdate, EnterpriseUpdate, EnterpriseProposalList

app_name='slavaukraine'
urlpatterns = [
    #http://127.0.0.1:8000/slavaukraine
    path("",views.home_screen, name="home"),

    #Área de Registos
    path("register_person",views.personRegistration_view, name="registerperson"),
    path("register_enterprise", views.enterpriseRegistration_view, name="registerenterprise"),
    path("regist_proposal/", views.proposal_create_view, name="registproposal"),
        #O PATH em baixo é um auxiliar do regist_proposal, na dropdown dinâmica;
        path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),

    #Área de edição
    path("editPerson/<int:pk>/", ProposalUpdate.as_view(), name='edit_person'),
    path("editEnterprise/<int:pk>/", EnterpriseUpdate.as_view(), name='edit_enterprise'),
    path("editPerson/<int:pk>/", ProposalUpdate.as_view(), name='edit_person'),
    path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),   #AJAX

    #Área de Listagens
    # http://127.0.0.1:8000/slavaukraine/listed_proposals
    path("listed_proposals/<int:pk>/", EnterpriseProposalList.as_view(), name='listed_enterpriseproposals'),
    path("listed_proposals/<int:pk>/", ProposalList.as_view(), name='listed_proposals'),
    #EM FALTA: Favoritos do User, Inscrições do User, Inscrições na Proposta X da Empresa Y



    #http://127.0.0.1:8000/slavaukraine/login
    path("login/",views.login_view, name="login"),

    #http://127.0.0.1:8000/slavaukraine/logout
    path("logout/",views.logout_view, name="logout"),

    #http://127.0.0.1:8000/slavaukraine/logout
    path("reserved",views.reserved, name="reserved"),

    #http://127.0.0.1:8000/slavaukraine/volunteer
    path("volunteer",views.volunteer, name="volunteer"),

    #http://127.0.0.1:8000/slavaukraine/enterprise
    path("enterprise",views.enterprise, name="enterprise"),

    #http://127.0.0.1:8000/slavaukraine/contacts
    path("contacts",views.contacts, name="contacts"),



]

"""from django.urls import include, path
from . import views



app_name='slavaukraine'
urlpatterns = [
    #http://127.0.0.1:8000/slavaukraine
    path("",views.home_screen, name="home"),

    #http://127.0.0.1:8000/slavaukraine/register_person
    path("register_person",views.personRegistration_view, name="registerperson"),

    # http://127.0.0.1:8000/slavaukraine/register_enterprise
    path("register_enterprise", views.enterpriseRegistration_view, name="registerenterprise"),

    # http://127.0.0.1:8000/slavaukraine/regist_proposal
    path("regist_proposal/", views.proposal_create_view, name="registproposal"),
    #path("<int:pk>/", views.proposal_create_view, name="registproposal"),

    path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),   #AJAX

    path("list_proposals", views.listProposals_view, name="list_proposals"),
    path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),   #AJAX

    #http://127.0.0.1:8000/slavaukraine/login
    path("login/",views.login_view, name="login"),

    #http://127.0.0.1:8000/slavaukraine/logout
    path("logout/",views.logout_view, name="logout"),

    #http://127.0.0.1:8000/slavaukraine/logout
    path("reserved",views.reserved, name="reserved"),

    #http://127.0.0.1:8000/slavaukraine/volunteer
    path("volunteer",views.volunteer, name="volunteer"),

    #http://127.0.0.1:8000/slavaukraine/enterprise
    path("enterprise",views.enterprise, name="enterprise"),

    #http://127.0.0.1:8000/slavaukraine/contacts
    path("contacts",views.contacts, name="contacts"),
]"""
