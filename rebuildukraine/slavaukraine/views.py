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
from django.http import HttpResponse, JsonResponse

from .models import Person, TopicMessage
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
                return render(request, 'slavaukraine/reserved.html');
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
    return render(request, 'slavaukraine/register_person.html', context)

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
    return render(request, 'slavaukraine/register_enterprise.html', context)



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
            return render(request, 'slavaukraine/reserved.html');
    return render(request, 'slavaukraine/registproposal.html', {'form': form});

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

class EnterpriseProposalList(ListView):
    model = Proposal
    template_name = 'slavaukraine/reserved.html'
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
                return view_profile(request)
    #If they are not authenticated and they didnt try to loggin yet...
    else:
        form = PersonAuthenticationForm
    print("Chegou aqui!")
    context['login_form'] = form
    return render(request, 'slavaukraine/login.html',context)

def view_profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'slavaukraine/reserved.html', context)




#pagina de contactos
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

def submitContact(request):
    subjet = "From:" + request.POST.get('name')
    email = request.POST.get('email')
    text = request.POST.get('message')
    print(" nome " + subjet)
    print(" email " + email)
    print("text " + text)
    send_mail(subjet,text,'slavaukraine@sapo.pt',[email])
    print("enviou")
    return home_screen(request)




# Area reservada
def reserved(request):
    return render(request, 'slavaukraine/reserved.html')

# pagina de mais informações sobre ser voluntário
def volunteer(request):
    return render(request, 'slavaukraine/volunteers.html')

# pagina de mais informações sobre empresa
def enterprise(request):
    return render(request, 'slavaukraine/enterprise.html')

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


def proposal_view(request):
    context = {}
    context["dataset"] = Proposal.objects.all()
    return render(request, 'slavaukraine/test_Porposal_List.html', context)

#Só para teste
def porposal_detail(request, proposal_id):
    proposal = get_object_or_404(Proposal, pk=proposal_id)
    context = {'proposal': proposal}
    return render(request, 'slavaukraine/test_Porposal.html', context)


# view para listar todas as mensagens

def viewMessages(request):
    if True: #getUser(request):
        list = TopicMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-date')
        context = {
            'list' : list
        }
        print("chegou")
        return render(request, 'slavaukraine/viewMessages.html', context)
    else:
        return home_screen(request)  # vai para a home


# view da nova msg entre user
def newMessage(request,recipient):
    if request.POST:
        print("entrou 2")
        if utils.getUser(request):
            topic = utils.saveMessage(request, recipient) # cria o titulo ou topico da mensagem
            utils.saveReply(request, topic, Person.objects.get(id=recipient)) #cria a mensagem ou resposta
            utils.send_newMessage(request,Person.objects.get(id=recipient)) # envia email para o user
            context={
                'recipient': recipient
            }
            return render(request, 'slavaukraine/create_new_message.html',context)
        else:
            return home_screen(request) # vai para a home
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
            return home_screen(request) # vai para a home
    else:
        return None # retornar a pagina