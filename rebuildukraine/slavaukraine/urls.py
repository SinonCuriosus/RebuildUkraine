from django.urls import include, path
from . import views



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
    path("editProposal/<int:pk>/", ProposalUpdate.as_view(), name='edit_proposal'),


    #Área de Listagens
    # http://127.0.0.1:8000/slavaukraine/listed_proposals
    path("listed_proposals/<int:pk>/", EnterpriseProposalList.as_view(), name='listed_enterpriseproposals'),
    path("listed_proposals/<int:pk>/", ProposalList.as_view(), name='listed_proposals'),
    #EM FALTA: Favoritos do User, Inscrições do User, Inscrições na Proposta X da Empresa Y

    #Área de remoção


    #http://127.0.0.1:8000/slavaukraine/login
    path("login/",views.login_view, name="login"),

    #http://127.0.0.1:8000/slavaukraine/logout
    path("logout/",views.logout_view, name="logout"),

    #http://127.0.0.1:8000/slavaukraine/logout
    path("reserved",views.reserved, name="reserved"),

    #http://127.0.0.1:8000/slavaukraine/volunteer
    path("volunteer",views.volunteer, name="volunteer"),

    #http://127.0.0.1:8000/slavaukraine/volunteer/edit_volunteer_page
    path("volunteer/edit_volunteer_page",views.edit_volunteer_page, name="edit_volunteer_page"),

    #http://127.0.0.1:8000/slavaukraine/enterprise
    path("enterprise",views.enterprise, name="enterprise"),

    #http://127.0.0.1:8000/slavaukraine/contacts
    path("contacts",views.contacts, name="contacts"),

    #http://127.0.0.1:8000/slavaukraine/Porposal_List
    path("test_Porposal_List",views.proposal_view, name="test_Porposal_List"),

    #teste
    path('<int:proposal_id>', views.porposal_detail, name="test_Porposal"),

    path('<int:proposal_id>/register_porposal', views.register_proposal, name="register_porposal"),


    path("submitcontact",views.submitContact, name="submitcontact"),

    path("reserved/view_my_messages", views.viewMessages, name="view_my_messages"),

    path("reserved/create_new_message",views.newMessage, name="create_new_message"),

    ##
    ## Adicionar o id da messagem
    ##

    path("reply_message",views.newMessage, name="reply_message"),

]
