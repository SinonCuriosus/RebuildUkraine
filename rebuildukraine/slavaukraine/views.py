from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import PersonRegistrationForm, PersonAuthenticationForm
from django.http import HttpResponse

#We must import our objects structure, so we can work them
#example... Using : Person.objects.all() to list all people
from .models import Person
from .models import Enterprise
from .models import Country
from .models import City
from .models import Expertise
from .models import Specialization
from .models import Proposal
from .models import Favorites
from .models import Registration

# Create your views here.

def home_screen(request):
    if request.user.is_authenticated & request.user.is_active:
        name_user = request.user.first_name + " " + request.user.last_name
        is_authenticated = 1
        role_user = request.user.is_person
    else:
        print("anonymous")
        name_user = "anonymous"
        is_authenticated = 0
        role_user = 0
    context = {
        'title': 'Building Ukraine - Homepage ',
        'name_user': name_user,
        'role_user': role_user,
        'is_authenticated': is_authenticated
    }
    return render(request, 'slavaukraine/home.html',context);

def login_view(request):
    context={}
    if request.POST:
        return 0
    return render(request, 'slavaukraine/login.html')

def personRegistration_view(request):
    context={}
    if request.POST:
        form = PersonRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email= form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            person = authenticate(email=email, password=raw_password)
            login(request,person)
            return home_screen(request)
        else:
            context['personregistration_form'] = form
    else:
        form = PersonRegistrationForm
        context['personregistration_form'] = form
    return render(request, 'slavaukraine/register.html', context)
    #return render(request, 'slavaukraine/register_test.html', context)

def logout_view(request):
    logout(request)
    return home_screen(request)

def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return home_screen(request)
    if request.POST:
        form = PersonAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return home_screen(request)
    #If they are not authenticated and they didnt try to loggin yet...
    else:
        form = PersonAuthenticationForm
    context['login_form'] = form
    return render(request, 'slavaukraine/login.html',context)




#pagina de contactos
def contacts(request):
    if request.user.is_authenticated & request.user.is_active:
        name_user = request.user.first_name + " " + request.user.last_name
        is_authenticated = 1
        role_user = request.user.is_person
    else:
        print("anonymous")
        name_user = "anonymous"
        is_authenticated = 0
        role_user = 0
    context = {
        'title': 'Building Ukraine - Contactos',
        'name_user': name_user,
        'role_user': role_user,
        'is_authenticated': is_authenticated
    }
    return render(request, 'slavaukraine/contacts.html',context)





# Area reservada
def reserved(request):
    return render(request, 'slavaukraine/reserved.html')

# pagina de mais informações sobre ser voluntário
def volunteer(request):
    return None

# pagina de mais informações sobre empresa
def enterprise(request):
    return None