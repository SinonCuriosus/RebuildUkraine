from django.urls import include, path
from django.views.generic import DeleteView

from . import views
from .views import ProposalList, ProposalUpdate, EnterpriseProposalList, EnterpriseUpdate, ProposalDelete, PersonUpdate, \
    PersonProposalList

app_name='slavaukraine'
urlpatterns = [
    # Paginas de apresentação da página
    path("",views.home_screen, name="home"),
    # mais info de voluntario
    path("volunteer", views.volunteer, name="volunteer"),
    # mais info de empresas
    path("enterprise",views.enterprise, name="enterprise"),
    # Contactos
    path("contacts",views.contacts, name="contacts"),
    # Login
    path("login/",views.login_view, name="login"),
    # Logout
    path("logout/",views.logout_view, name="logout"),
    #area reservada
    path("reserved_area", views.reserved, name="reserved_area"),


    # --------------------------------------------------------------------------------

    # ------------------------------ Voluntarios -------------------------------------

    # --------------------------------------------------------------------------------

    # Área de Registos
    path("register_person", views.personRegistration_view, name="registerperson"),

    # Área de edição
    path("editPerson/<int:pk>/", PersonUpdate.as_view(), name='edit_person'),

    # --------------------------------------------------------------------------------

    # -------------------------------- Empresas ---------------------------------------

    # --------------------------------------------------------------------------------

    # Registo da empresa
    path("register_enterprise", views.enterpriseRegistration_view, name="registerenterprise"),
    # Registo de proposta
    path("regist_proposal/", views.proposal_create_view, name="registproposal"),
        #O PATH em baixo é um auxiliar do regist_proposal, na dropdown dinâmica;
        path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),

    # Edição user Empresarial
    path("editEnterprise/<int:pk>/", EnterpriseUpdate.as_view(), name='enterprise'),
    # Edição proposta da empresa
    path("editProposal/<int:pk>/", ProposalUpdate.as_view(), name='edit_proposal'),


    #Área de Listagens
    path("listed_proposals/<int:pk>/", EnterpriseProposalList.as_view(), name='list_enterpriseproposals'),
    path("listed_proposals/<int:pk>/", PersonProposalList.as_view(), name='list_personproposals'),
    path("listproposals/", ProposalList.as_view(), name='listproposals'),
    path("Registration_Volunteer_List", views.registration_volunteer_list, name="Registration_Volunteer_List"),
    path("Favorites_Volunteer_List", views.favorites_volunteer_list, name="Favorites_Volunteer_List"),
    #EM FALTA: Inscrições na Proposta X da Empresa Y

    #Área de remoção

    path("deleteProposal/<int:pk>/", ProposalDelete.as_view(), name='delete_proposal'),

    # --------------------------------------------------------------------------------

    # --------------------------- Serviço de Emails ----------------------------------

    # --------------------------------------------------------------------------------

    #http://127.0.0.1:8000/slavaukraine/Porposal_List
    path("test_Porposal_List",views.proposal_view, name="test_Porposal_List"),


    # Verificar as mensagens dos users
    path("reserved/view_my_messages", views.viewMessages, name="view_my_messages"),
    # Criar uma nova mensagem para o user
    path("reserved/create_new_message/<int:recipient>", views.newMessage, name="create_new_message"),

    ##
    ## Adicionar o id da messagem
    ##
    # Resposta à mensagem
    path("reserved/reply_message/<int:topic>", views.newMessage, name="reply_message"),



    #Proposta detalhe
    path('<int:proposal_id>', views.proposal_detail, name="proposal"),
    
    #Registar em proposta
    path('<int:proposal_id>/register_porposal', views.register_proposal, name="register_porposal"),
    
    #Adicionar aos favoritos
    path('<int:proposal_id>/favorite_proposal', views.favorite_proposal, name="favorite_proposal"),



]
