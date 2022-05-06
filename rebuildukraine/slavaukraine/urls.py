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

    #http://127.0.0.1:8000/slavaukraine/enterprise
    path("enterprise",views.enterprise, name="enterprise"),

    #http://127.0.0.1:8000/slavaukraine/contacts
    path("contacts",views.contacts, name="contacts"),

    path("submitcontact",views.submitContact, name="submitcontact"),

    path("reserved/view_my_messages", views.viewMessages, name="view_my_messages"),

    path("reserved/create_new_message",views.newMessage, name="create_new_message"),

    ##
    ## Adicionar o id da messagem
    ##

    path("reply_message",views.newMessage, name="reply_message"),

]
