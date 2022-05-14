import copy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from . import forms, utils
from .forms import PersonRegistrationForm, PersonAuthenticationForm, EnterpriseRegistrationForm, ProposalForm
from .models import Person, TopicMessage
from .models import City
from .models import Proposal
from .models import Favorites
from .models import Registration

# Create your views here.

#Pagina inicial -RR visto
def home(request):
    last_proposals = utils.getLastThreeProposal()
    for proposal in last_proposals:
        print(proposal.title)
    context = {
        'title': 'Building Ukraine - Homepage',
        'last_proposals': last_proposals
    }
    return render(request, 'slavaukraine/home.html', context);

# pagina de mais informações sobre ser voluntário -RR visto
def volunteer(request):
    context = {
        'title': 'Building Ukraine - Ser Voluntário',
    }
    return render(request, 'slavaukraine/volunteers.html', context)

# pagina de mais informações sobre empresa -RR visto
def enterprise(request):
    context = {
        'title': 'Building Ukraine - Apresentar Projetos',
    }
    return render(request, 'slavaukraine/enterprise.html')

#pagina de contactos-RR visto
def contacts(request):
    if request.POST:
        subjet = "From:" + request.POST.get('name')
        email = request.POST.get('email')
        text = request.POST.get('message')
        send_mail(subjet, text, 'slavaukraine@sapo.pt', [email])
        context = {
            'title': 'Building Ukraine - Contactos',
            'enviado': 1
        }
        return render(request, 'slavaukraine/contacts.html',context)
    else:
        context = {
            'title': 'Building Ukraine - Contactos',
            'enviado': 0
        }
        return render(request, 'slavaukraine/contacts.html',context)


# Logout -RR visto
def logout_view(request):
    logout(request)
    return home(request)

# Login -RR visto
def login_view(request):
    if request.POST:
        form = PersonAuthenticationForm(request.POST)
        context = {
            'title': 'Building Ukraine - Login',
            'login_form': form
        }
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return home(request)
            else:
                return render(request, 'slavaukraine/login.html', context)
        else:
            return render(request, 'slavaukraine/login.html', context)
    else:
        if utils.verifyUser(request):
            return home(request)
        else:
            form = PersonAuthenticationForm
            context = {
                'title': 'Building Ukraine - Login',
                'login_form': form
            }
            return render(request, 'slavaukraine/login.html',context)

# Area reservada
def reserved(request):
    list = utils.getUserMEssages(request)
    proposals = utils.getProposals(request)
    favorites = utils.getFavorites(request)
    context = {
        'title': 'Building Ukraine - Área Reservada',
        'list': list,
        'proposals': proposals,
        'favorites': favorites
    }
    return render(request, 'slavaukraine/reserved.html',context)

# Registo de Empresa
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
            return home(request)
        else:

            context['enterpriseregistration_form'] = form
    else:
        form = EnterpriseRegistrationForm()
        context['enterpriseregistration_form'] = form
    return render(request, 'slavaukraine/register_enterprise.html', context)


# Registo de Voluntarios
def volunteerRegistration_view(request):
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
            return home(request)
        else:
            context['personregistration_form'] = form
    else:
        form = PersonRegistrationForm()
        context['personregistration_form'] = form
    return render(request, 'slavaukraine/register_volunteer.html', context)


# Pagina de registo de proposta
def proposal_create_view(request):
    if utils.isEnterprise(request):
        enterprise = get_object_or_404(Person, pk=request.user.pk)
        form = ProposalForm(initial={'enterprise': enterprise})
        if request.method == 'POST':
        #We need to do a copy of the form data from the request, because Forms are IMMUTABLE.
            form_data = copy.copy(request.POST)
            form_data['enterprise'] = enterprise.id
            form = ProposalForm(data=form_data)
            if form.is_valid():
                form.save()
                return render(request, 'slavaukraine/reserved.html');
        else:
            context = {
                'title': 'Building Ukraine - Registo de Proposta',
                'form': form
            }
            return render(request, 'slavaukraine/regist_proposal.html', context);
    else:
        return render(request, 'slavaukraine/home.html')


#aux para alimentar a pagina de criaçao de propostas
def load_cities(request):
    country_id = request.GET.get('country_id')
    cities = City.objects.filter(country_id=country_id)
    return render(request,'slavaukraine/city_dropdown_list_options.html',{'cities':cities})


# List view de todas as propostas
class ProposalList(ListView):
    model = Proposal
    template_name = 'slavaukraine/listproposals.html'
    paginate_by = 10
    def get_queryset(self):
        proposal_title_inserted = self.request.GET.get('nome_do_titulo')
        if proposal_title_inserted:
            proposals = Proposal.objects.filter(title__icontains=proposal_title_inserted)
        else:
            proposals = Proposal.objects.all()
        return proposals

















###############     UPDATE VIEWS   ###############
class ProposalUpdate(UpdateView):
    model = Proposal
    fields = ['title','expertiseNeeded','description']
    template_name = 'slavaukraine/edituser.html'

    def get_success_url(self):
        return reverse('slavaukraine:home')


class PersonUpdate(UpdateView):
    model = Person
    fields = ['first_name', 'last_name','profile_image','gender','address','birth']
    template_name = 'slavaukraine/reserved.html'
    success_url = reverse_lazy('slavaukraine:home')

class EnterpriseUpdate(UpdateView):
    model = Person
    fields = ['email','first_name','taxnumber','profile_image','address']
    template_name = 'slavaukraine/edituser.html'
    success_url = reverse_lazy('slavaukraine:home')



###############     DELETE VIEWS   ###############
class ProposalDelete(DeleteView):
    model = Proposal
    template_name = 'slavaukraine/deleteproposal.html'
    #success_url = reverse_lazy('slavaukraine:listed_proposals')

    def get_success_url(self, **kwargs):
        return reverse('slavaukraine:home')

###############     LIST VIEWS     ###############



class EnterpriseProposalList(ListView):
    model = Proposal
    template_name = 'slavaukraine/test_datatable.html'
    #slavaukraine / listed_proposals / 3
    paginate_by = 10


    def get_queryset(self):
        enterprise = self.request.user
        proposal_title_inserted = self.request.GET.get('nome_do_titulo')
        if proposal_title_inserted:
            proposals = Proposal.objects.filter(enterprise_id=enterprise.id).filter(title__icontains=proposal_title_inserted)
        else:
            proposals = Proposal.objects.filter(enterprise_id=enterprise.id)
        return proposals


#Proposals by user
class PersonProposalList(ListView):
    model = Proposal
    template_name = 'slavaukraine/reserved.html'
    paginate_by = 10
    
    def get_queryset(self):
        person = self.request.user
        proposal_title_inserted = self.request.GET.get('nome_do_titulo')
        if proposal_title_inserted:
            proposals = Proposal.objects.filter(person_id=person.id).filter(title__icontains=proposal_title_inserted)
        else:
            proposals = Proposal.objects.filter(person_id=person.id)
        return proposals







# Area reservada
def reserved(request):
    list = utils.getUserMEssages(request)
    proposals = utils.getProposals(request)
    proposals_enterpise = utils.getProposalsEnterprise(request)
    favorites = utils.getFavorites(request)
    context = {
        'title': 'Building Ukraine - Área Reservada',
        'list': list,
        'proposals': proposals,
        'proposals_enterprise': proposals_enterpise,
        'favorites': favorites
    }
    return render(request, 'slavaukraine/reserved.html',context)

# pagina de mais informações sobre ser voluntário -RR visto
def volunteer(request):
    context = {
        'title': 'Building Ukraine - Ser Voluntário',
    }
    return render(request, 'slavaukraine/volunteers.html', context)

# pagina de mais informações sobre empresa -RR visto
def enterprise(request):
    context = {
        'title': 'Building Ukraine - Apresentar Projetos',
    }
    return render(request, 'slavaukraine/enterprise.html')

# Visualização da proposta
def viewProposal(request,proposal_id):
    print("proposal")
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    if request.POST:
        print("post")
        if utils.verifyUser(request):
            print("verificado")
            regist = Registration()
            regist.proposal_id = proposal_id
            print(proposal_id)
            regist.person_id=request.user.id
            print(request.user.id)
            regist.save()
            registed = 1
        else:
            registed = 0
    else:
        registed = utils.isRegisted(request, proposal_id)
    context = {
            'title': 'Building Ukraine - Visualização Proposta',
            'proposal': proposal,
            'registed': registed,
    }
    return render(request,'slavaukraine/proposal.html', context)






# voluntario remove propostaw
def unregister_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.unregister(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/reserved.html', context)
    else:
        return login_view(request)

#voluntario coloca proposta nos favoritos
def favorite_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.subscribe(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/reserved.html', context)
    else:
        return login_view(request)


# voluntario remove dos favoritos
def not_favorite_proposal(request, proposal_id):
    if request.user.is_authenticated & request.user.is_active:  # Alterar por decorator
        proposal = get_object_or_404(Proposal, pk=proposal_id)
        proposal.unsubscribe(user=request.user)
        context = {'proposal': proposal}
        return render(request, 'slavaukraine/reserved.html', context)
    else:
        return login_view(request)

def registration_volunteer_list(request):
    context = {}
    context["dataset"] = Proposal.objects.filter(registration__person__username=request.user)
    return render(request, 'slavaukraine/reserved.html', context)


def favorites_volunteer_list(request):
    context = {}
    context["dataset"] = Favorites.objects.filter(favorites__person__username=request.user)
    return render(request, 'slavaukraine/reserved.html', context)

def proposal_view(request):
    context = {}
    context["dataset"] = Proposal.objects.all()
    return render(request, 'slavaukraine/test_Porposal_List.html', context)

#Só para teste
def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    context = {'proposal': proposal}
    return render(request, 'slavaukraine/proposal.html', context)


# view para listar todas as mensagens - Possivelmente para remover
def viewMessages(request):
    if True: #getUser(request):
        list = TopicMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-date')
        context = {
            'title': 'Building Ukraine - Homepage',
            'list' : list
        }
        return render(request, 'slavaukraine/viewMessages.html', context)
    else:
        return home(request)


# view da nova msg entre user
def newMessage(request,recipient):
    if request.POST:
        print("entrou 2")
        if utils.verifyUser(request):
            topic = utils.saveMessage(request, recipient) # cria o titulo ou topico da mensagem
            utils.saveReply(request, topic, Person.objects.get(id=recipient)) #cria a mensagem ou resposta
            utils.send_newMessage(request,Person.objects.get(id=recipient)) # envia email para o user
            context={
                'recipient': recipient
            }
            return render(request, 'slavaukraine/create_new_message.html',context)
        else:
            return home(request) # vai para a home
    else:
        context = {
            'recipient': recipient,
            'to_name': Person.objects.get(id=recipient)
        }
        return render(request,'slavaukraine/create_new_message.html',context)


# view da reposta as mensagens
def replyMessage(request,recipient, topic):
    if request.POST:
        if utils.getUser(request):
            utils.saveReply(request, topic, recipient) #cria a mensagem ou resposta
            utils.send_replyMessage(request,recipient) # envia email para o user
            # return para a view dos emails
        else:
            return home(request) # vai para a home
    else:
        return None # retornar a pagina