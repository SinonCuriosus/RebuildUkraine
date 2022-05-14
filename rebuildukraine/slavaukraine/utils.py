from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import TopicMessage, Answers, Person, Proposal, Registration


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
    topic.subjet = request.POST['subjet']
    topic.sender = request.user
    topic.receiver = Person.objects.get(id=recipient)
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

# obtem as propostas
def getProposals(request):
    return  Proposal.objects.filter(registration__person__username=request.user.username)

# Obtem os favoritos
def getFavorites(request):
    return Proposal.objects.filter(favorites__person__username=request.user.username)

# verifica se está registado na proposta
def isRegisted(request,proposal_id):
    registed = Registration.objects.filter((Q(proposal=proposal_id) & Q(person=request.user.id)))
    if registed is None:
        return 0
    else:
        return 1

def getLastThreeProposal():
    return Proposal.objects.filter().order_by('-id')[:4]



def partOfTopic(request,topic_id):
    topic = TopicMessage.objects.filter(pk=topic_id).first()
    if (topic.sender == request.user):
        return True
    else:
        if(topic.receiver == request.user):
            return True
        else:

            return False


def getSender(request,topic_id):
    topic = TopicMessage.objects.filter(pk=topic_id).first()
    if (topic.sender == request.user):
        return topic.receiver
    else:
        return topic.sender


def getTopicMessages(topic_id):
    return Answers.objects.filter(Q(topic_id=topic_id))