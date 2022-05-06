import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout

from . import forms
from .forms import PersonRegistrationForm, PersonAuthenticationForm, EnterpriseRegistrationForm, ProposalForm
from django.http import HttpResponse, JsonResponse

from .models import Person
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
        name_user=request.user.username
        if request.user.is_enterprise:
                list_of_proposals = Proposal.objects.filter(enterprise__email=request.user.email)
                context = {
                    # 'title': 'Building Ukraine - Homepage ',
                    'name_user': name_user,
                    # 'role_user': role_user,
                    # 'is_authenticated': is_authenticated
                    'list_of_proposals': list_of_proposals
                }
                return render(request, 'slavaukraine/test_home.html', context);
    else:
        name_user = "anonymous"
    context = {
        #'title': 'Building Ukraine - Homepage ',
        'name_user': name_user,
        #'role_user': role_user,
        #'is_authenticated': is_authenticated
    }
    return render(request, 'slavaukraine/test_home.html', context);
"""
def login_view(request):
    context={}
    if request.POST:
        return 0
    return render(request, 'slavaukraine/login.html')"""

def personRegistration_view(request):
    context={}
    if request.POST:
        form = PersonRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email= form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            person = authenticate(email=email, password=raw_password)
            person.setPerson()
            login(request,person)
            return home_screen(request)
        else:
            context['personregistration_form'] = form
    else:
        form = PersonRegistrationForm()
        context['personregistration_form'] = form
    return render(request, 'slavaukraine/test_registeruser.html', context)

def enterpriseRegistration_view(request):
    context={}
    if request.POST:
        form = EnterpriseRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email= form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            person = authenticate(email=email, password=raw_password)
            #person.setEnterprise()
            login(request,person)
            return home_screen(request)
        else:

            context['enterpriseregistration_form'] = form
    else:
        form = EnterpriseRegistrationForm()
        context['enterpriseregistration_form'] = form
    return render(request, 'slavaukraine/test_registerenterprise.html', context)

def listProposals_view(request):
    if request.user.is_authenticated:
        list_of_proposals = Proposal.objects.filter(enterprise__email=request.user.email)
        return render(request, 'slavaukraine/test_home.html',{'list_of_proposals':list_of_proposals});
    return render(request, 'slavaukraine/test_home.html')

def proposal_create_view(request):
    enterprise = get_object_or_404(Person, pk=request.user.pk)
    form = ProposalForm(initial={'enterprise': enterprise})

    if request.method == 'POST':
        #We need to do a copy of the form data from the request, because Forms are IMMUTABLE.
        form_data = copy.copy(request.POST)
        form_data['enterprise'] = enterprise.id
        form = ProposalForm(data=form_data)
        if form.is_valid():
            print("É VÁLIDO")
            form.save()
            return render(request, 'slavaukraine/test_home.html');
    return render(request, 'slavaukraine/test_registproposal.html', {'form': form});


def load_cities(request):
    country_id = request.GET.get('country_id')
    print("VIEWS: load_cities RESULT:")
    print(country_id)
    cities = City.objects.filter(country_id=country_id)
    #return render(request, 'proposals/city_dropdown_list_options.html', {'cities':cities})
    #Way of get to know the info we are sending: print(list(cities.values('id','name')))
    return render(request,'slavaukraine/city_dropdown_list_options.html',{'cities':cities})
    #return JsonResponse(list(cities.values('id','name')), safe=False)
"""
def registProposal(request):
    expertises = Expertise.objects.all();
    if request.POST and request.user.is_enterprise:
        enterprise = request.user;
        city = request.POST.get('city')
        expertise = request.POST.get('expertise')
        description = request.POST.get('description')
        proposal = Proposal(enterprise=enterprise,city=city,expertiseNeeded=expertise,description=description)
        proposal.save()
        return render(request, 'slavaukraine/test_home.html')
    else:
        return render(request, 'slavaukraine/test_registproposal.html')"""


def logout_view(request):
    logout(request)
    return home_screen(request)

def login_view(request):
    context={}
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
        #name_user = request.user.first_name + " " + request.user.last_name
        name_user = request.user.username
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
    return render(request, 'slavaukraine/contacts.html')





# Area reservada
def reserved(request):
    return render(request, 'slavaukraine/reserved.html')

# pagina de mais informações sobre ser voluntário
def volunteer(request):
    return None

# pagina de mais informações sobre empresa
def enterprise(request):
    return None