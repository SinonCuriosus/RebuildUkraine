import copy

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.views.generic import UpdateView, ListView, DeleteView

from . import forms
from .forms import PersonRegistrationForm, PersonAuthenticationForm, EnterpriseRegistrationForm, ProposalForm
from django.http import HttpResponse, request

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
                return render(request, 'slavaukraine/home.html');
    else:
        name_user = "anonymous"
    context = {
        #'title': 'Building Ukraine - Homepage ',
        'name_user': name_user,
        #'role_user': role_user,
        #'is_authenticated': is_authenticated
    }
    return render(request, 'slavaukraine/home.html', context);

###############     REGIST VIEWS   ###############

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

#Do not delete, It's a helper to Create proposals; Does the adaptative dropdown in the city.
def load_cities(request):
    country_id = request.GET.get('country_id')
    print("VIEWS: load_cities RESULT:")
    print(country_id)
    cities = City.objects.filter(country_id=country_id)
    #return render(request, 'proposals/city_dropdown_list_options.html', {'cities':cities})
    #Way of get to know the info we are sending: print(list(cities.values('id','name')))
    return render(request,'slavaukraine/city_dropdown_list_options.html',{'cities':cities})
    #return JsonResponse(list(cities.values('id','name')), safe=False)

###############     UPDATE VIEWS   ###############
class ProposalUpdate(UpdateView):
    model = Proposal
    fields = ['title','expertiseNeeded','description']
    template_name = 'slavaukraine/test_edituser.html'
    success_url = '../../listed_proposals'

class PersonUpdate(UpdateView):
    model = Person
    fields = ['email','first_name', 'last_name','tax_number','profile_image','gender','address','birth']
    template_name = 'slavaukraine/test_edituser.html'
    success_url = '../../home'

class EnterpriseUpdate(UpdateView):
    model = Person
    fields = ['email','first_name','taxnumber','profile_image','address']
    template_name = 'slavaukraine/test_editproposal.html'
    success_url = '../../home'



###############     DELETE VIEWS   ###############
class ProposalDelete(DeleteView):
    model = Proposal
    template_name = 'slavaukraine/test_deleteproposal.html'
    success_url = '../../listed_proposals'


###############     LIST VIEWS     ###############

#All proposals
class ProposalList(ListView):
    #  login_url = reverse_lazy('test_login')
    model = Proposal
    template_name = 'slavaukraine/test_listedproposals.html'
    paginate_by = 10

"""
    def get_queryset(self):

        proposal_name_inserted = self.request.POST.get('nome_do_titulo')
        enterprise_user = self.request.user
        if proposal_name_inserted:
            proposals = Proposal.objects.filter(enterprise_id=enterprise_user.id).filter(title__icontains=proposal_name_inserted)
        else:
            proposals = Proposal.objects.all().filter()
        return proposals"""

#Proposals by enterprise
class EnterpriseProposalList(ListView):
    model = Proposal
    template_name = 'slavaukraine/test_listedproposals.html'
    paginate_by = 10

    def get_queryset(self):
        enterprise = self.request.user
        queryset = Proposal.objects.filter(enterprise_id=enterprise.id)
        return queryset

#Proposals by user
class PersonProposalList(ListView):
    model = Proposal
    template_name = 'slavaukraine/test_home.html'

    def get_queryset(self):
        queryset = super(PersonProposalList, self.get_queryset())
        queryset = queryset.filter(user=self.request.user)
        return queryset


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

#voluntario regista-se em propostas
def register_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.register(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/test_Porposal.html', context)
    else:
        return login_view(request)


# voluntario remove proposta
def unregister_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.unregister(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/test_Porposal.html', context)
    else:
        return login_view(request)

#voluntario coloca proposta nos favoritos
def favorite_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.subscribe(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/test_Porposal.html', context)
    else:
        return login_view(request)


# voluntario remove dos favoritos
def not_favorite_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.unsubscribe(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/test_Porposal.html', context)
    else:
        return login_view(request)

def edit_volunteer_page(request):
    return None


def registration_volunteer_list(request):
    context = {}
    context["dataset"] = Proposal.objects.filter(registration__person__username=request.user)
    return render(request, 'slavaukraine/test_Registration_Volunteer_List.html', context)


def favorites_volunteer_list(request):
    context = {}
    context["dataset"] = Favorites.objects.filter(favorites__person__username=request.user)
    return render(request, 'slavaukraine/test_Favorites_Volunteer_List.html', context)

#Só para teste
def porposal_detail(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    context = {'proposal': proposal}
    return render(request, 'slavaukraine/test_Porposal.html', context)
