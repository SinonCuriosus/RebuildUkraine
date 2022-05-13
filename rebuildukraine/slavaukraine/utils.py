import _datetime
import datetime

from django.core.mail import send_mail
from django.db.models import Q

from .models import TopicMessage, Answers, Person, Proposal, Favorites
from .models import TopicMessage, Answers, Person, Registration


def send_email(subjet,text,email):
    send_mail(subjet, text, 'slavaukraine@sapo.pt', [email])


def verifyUser(request):
    if request.user.is_authenticated & request.user.is_active:
        return True
    else:
        return False

def isEnterprise(request):
    if verifyUser(request):
        if request.user.is_enterprise:
            return True
        else:
            return False
    else:
        return False

def getUser(request):
    if verifyUser(request):
        return request.user.username
    else:
        return None

def saveMessage(request, recipient):
    topic = TopicMessage()
    print("subjet " + request.POST['subjet'])
    topic.subjet = request.POST['subjet']
    print("sender " + request.user.first_name)
    topic.sender = request.user
    print("receiver " + Person.objects.get(id=recipient).first_name)
    topic.receiver = Person.objects.get(id=recipient)
    print("salvar")
   # topic.date = _datetime.date.today()
    topic.isRead = True
    topic.save()
    return topic


# Cria a resposta
def saveReply(request, topic, recipient):
    reply = Answers()
    reply.topic = topic
    reply.message = request.POST['message']
    reply.sender = request.user
    reply.receiver = recipient
    #reply.topic.date = datetime.now()
    reply.topic.isRead = True
    reply.save()

# Envia email de MSG novas
def send_newMessage(request,receiver):
    name = request.user.first_name  + " " + request.user.last_name
    subjet = "Nova mensagem de " + name
    text = "Tem uma nova mensagem de " + name
    send_email(subjet,text,receiver.email)

# Envia email de resposta a MSG
def send_replyMessage(request,receiver):
    name = request.user.first_name  + " " + request.user.last_name
    subjet = "Nova resposta " + name
    text = "Tem uma nova resposta à mensagem enviada a " + name
    send_email(subjet,text,receiver.email)


# Obtem as mensagens do utilizador
def getUserMEssages(request):

    return TopicMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-date')

def getProposals(request):
    return  Proposal.objects.filter(registration__person__username=request.user.username)

def getFavorites(request):
    return Proposal.objects.filter(favorites__person__username=request.user.username)
def isRegisted(request,proposal_id):
    registed = Registration.objects.filter(Q(proposal=proposal_id) | Q(person=request.user.id))
    if registed is None:
        return 0
    else:
        return 1

