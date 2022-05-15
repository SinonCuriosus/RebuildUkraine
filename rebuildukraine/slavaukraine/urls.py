from django.urls import include, path
from django.views.generic import DeleteView

from . import views
from .views import ProposalList, ProposalUpdate, EnterpriseProposalList, EnterpriseUpdate, ProposalDelete, PersonUpdate, \
    PersonProposalList

app_name='slavaukraine'
urlpatterns = [
    # Paginas de apresentação da página
    path("", views.home, name="home"),
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
    path("reserved", views.reserved, name="reserved"),

    # Registo de Empresa
    path("register_enterprise", views.enterpriseRegistration_view, name="register_enterprise"),

    # Registo de Voluntario
    path("register_volunteer", views.volunteerRegistration_view, name="register_volunteer"),

    # Registo de proposta
    path("reserved/regist_proposal", views.proposal_create_view, name="regist_proposal"),

    # Visualizacao de proposta com Opção de Inscrição ou Add aos Favoritos
    path("proposal/<int:proposal_id>", views.viewProposal, name="proposal"),
    # Remoção da Proposta das Inscrições
    path("remProposal/<int:proposal_id>", views.removeProposalSubscription, name="removesubscription"),
    # Remoção da Proposta dos Favoritos
    path("remFavorite/<int:proposal_id>", views.removeFavoriteProposal, name="removefavorite"),


    # Área de edição
    path("reserved/editPerson/<int:pk>/", PersonUpdate.as_view(), name='edit_person'),


        #O PATH em baixo é um auxiliar do regist_proposal, na dropdown dinâmica;
        path("ajax/load-cities/", views.load_cities, name="ajax_load_cities"),

    # Edição user Empresarial
    path("reserved/editEnterprise/<int:pk>/", EnterpriseUpdate.as_view(), name='enterprise_edit'),
    # Edição proposta da empresa
    path("editProposal/<int:pk>/", ProposalUpdate.as_view(), name='edit_proposal'),


    #Área de Listagens
    path("listed_proposals/<int:pk>/", EnterpriseProposalList.as_view(), name='list_enterpriseproposals'),

    path("listed_proposals/<int:pk>/", EnterpriseProposalList.as_view(), name='test_datatable'),
    path("listed_proposals/<int:pk>/", PersonProposalList.as_view(), name='list_personproposals'),
    path("listproposals/", ProposalList.as_view(), name='listproposals'),

    #EM FALTA: Inscrições na Proposta X da Empresa Y

    #Área de remoção
    path("deleteProposal/<int:pk>/", ProposalDelete.as_view(), name='delete_proposal'),
    #Apagar Empresa
    path("deleteUser/<int:pk>/", views.deleteUser, name='delete_user'),
    path("deleteProposal/<int:pk>/", ProposalDelete.as_view(), name='delete_proposal'),

    # --------------------------------------------------------------------------------

    # --------------------------- Serviço de Emails ----------------------------------

    # --------------------------------------------------------------------------------


    # Criar uma nova mensagem para o user
    path("reserved/create_new_message/<int:recipient>", views.newMessage, name="create_new_message"),

    ##
    ## Adicionar o id da messagem
    ##
    # Resposta à mensagem
    path("reserved/message/<int:topic_id>", views.replyMessage, name="message"),

    
    #Adicionar aos favoritos
    path('<int:proposal_id>/favorite_proposal', views.favorite_proposal, name="favorite_proposal"),



]
