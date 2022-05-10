import _datetime
import datetime

from django.core.mail import send_mail

from .models import TopicMessage, Answers, Person


def send_email(subjet,text,email):
    send_mail(subjet, text, 'slavaukraine@sapo.pt', [email])


def verifyUser(request):
    if request.user.is_authenticated & request.user.is_active:
        return True
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