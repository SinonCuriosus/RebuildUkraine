from django.urls import include, path
from . import views



app_name='slavaukraine'
urlpatterns = [
    #http://127.0.0.1:8000/slavaukraine
    path("",views.home_screen, name="home"),

    #http://127.0.0.1:8000/slavaukraine/register
    path("register",views.personRegistration_view, name="registerperson"),

    # http://127.0.0.1:8000/slavaukraine/register_enterprise
    path("register_enterprise", views.enterpriseRegistration_view, name="registerenterprise"),

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
    
]
