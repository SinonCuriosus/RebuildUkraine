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
    # http://127.0.0.1:8000/slavaukraine/logout


    path("reserved",views.reserved, name="reserved"),

    path("volunteer",views.volunteer, name="volunteer"),

    path("enterprise",views.enterprise, name="enterprise"),

    path("contacts",views.contacts, name="contacts"),


]
