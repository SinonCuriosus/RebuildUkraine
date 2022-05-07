from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models import Model
from django.forms import DateInput
from django.utils import timezone

# Create your models here.
# Create your models here.

#Utilizadores da Aplicação



class MyPersonManager(BaseUserManager):
    #Se adicionar nos REQUIRED arguments do USER mais argumentos, tenho que acrescentar aqui também
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user



class Person(AbstractBaseUser):
    MALE='Male'
    FEMALE='Female'
    BINARY='Binary'
    NONBINARY='Nonbinary'
    OTHER='Other'
    GENDER = [
        (MALE,'Male'),
        (FEMALE,'Female'),
        (BINARY,'Binary'),
        (NONBINARY,'Nonbinary'),
        (OTHER,'Other'),
    ]
    email                       =models.EmailField(verbose_name="email", max_length=60, unique=True)
    username                    =models.CharField(max_length=30, unique=True)
    profile_image               =models.ImageField(null=True,blank=True)
    taxnumber                   =models.CharField( unique=True, max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
    date_joined                 =models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                  =models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                    =models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    is_enterprise               = models.BooleanField(null=True, blank=True)
    is_person                   = models.BooleanField(null=True, blank=True)
    first_name                  = models.CharField(max_length=30,null=True, blank=True)
    last_name                   = models.CharField(max_length=30,null=True, blank=True)
    gender                      = models.CharField(max_length=10,choices=GENDER,null=True, blank=True)
    address                     = models.CharField(max_length=150,null=True, blank=True)
    birth                       = models.DateField(null=True, blank=True)
#Se quisermos o login com o username invés do e-mail é substituir aqui
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    objects = MyPersonManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return  self.is_admin

    def has_module_perms(self, app_label):
        return True



    def setEnterprise(self):
        self.is_enterprise=True;
        self.is_person=False;

    def setPerson(self):
        self.is_enterprise=False;
        self.is_person=True;

    class Meta:
        abstract = False
        verbose_name= "Utilizadores singulares"
        verbose_name_plural= "Utilizadores singulares"


#Neste momento faz sentido ser um tuplo porque só temos um país. Contudo se virmos que há potencial
#para acrescentar países, criamos um método para adicionar campos e retiramos o tuplo;

class Country(models.Model):
    """UKRAINI='Ucrânia'
    COUNTRIES = [
        (UKRAINI,'Ucrânia'),
    ]"""
    name                     =models.CharField(max_length=25)#,choices=COUNTRIES

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= "País"
        verbose_name_plural= "Países"



class City(models.Model):
    """KIEV='Kiev'
    KHARKIV='Kharkiv'
    MARIUPOL='Mariupol'
    CITIES = [
        (KIEV,'Kiev'),
        (KHARKIV,'Kharkiv'),
        (MARIUPOL,'Mariupol'),
    ]"""
    country                     =models.ForeignKey(Country, on_delete=models.CASCADE)
    name                        =models.CharField(max_length=25)#choices=CITIES

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= "Cidade"
        verbose_name_plural= "Cidades"


class Expertise(models.Model):
    name            =models.CharField(max_length=250)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name= "Especialização"
        verbose_name_plural= "Especializações"

class Specialization(models.Model):
    expertise                   = models.ForeignKey(Expertise,on_delete=models.CASCADE)
    person                      = models.ForeignKey(Person,on_delete=models.CASCADE)

    def __str__(self):
        return self.person.username

    class Meta:
        verbose_name= "Voluntário especialista"
        verbose_name_plural= "Voluntários especializados"

#Rever se acham que vale a pena só a cidade
class Proposal(models.Model):
    enterprise                  =models.ForeignKey(Person, on_delete=models.CASCADE)
    country                     =models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    city                        =models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    expertiseNeeded             =models.ForeignKey(Expertise,on_delete=models.CASCADE, blank=True, null=True)
    title                       =models.CharField(max_length=50)
    description                 =models.CharField(max_length=150)

    def __str__(self):
        return self.enterprise.username
    
    def register(self, user):
        registration = Registration.objects.create(person=user, proposal=self)
        return "Empresa: "+self.enterprise.username+" | Título: "+self.title

    def unregister(self, user):
        registration = Registration.objects.get(person=user, proposal=self)
        registration.delete()
        
    def subscribe(self, user):
        registration = Favorites.objects.create(person=user, proposal=self)

    def unsubscribe(self, user):
        registration = Favorites.objects.get(person=user, proposal=self)
        registration.delete()
        
    class Meta:
        verbose_name= "Proposta de voluntariado"
        verbose_name_plural= "Propostas de voluntariado"

class Favorites(models.Model):
    person                      = models.ForeignKey(Person,on_delete=models.CASCADE)
    proposal                    = models.ForeignKey(Proposal,on_delete=models.CASCADE)

    def __str__(self):
        return self.person.username

    class Meta:
        verbose_name= "Favorito"
        verbose_name_plural= "Favoritos"

class Registration(models.Model):
    person                      =models.ForeignKey(Person,on_delete=models.CASCADE)
    proposal                    =models.ForeignKey(Proposal,on_delete=models.CASCADE)

    def __str__(self):
        return self.person.username

    class Meta:
        verbose_name= "Registo em voluntariado"
        verbose_name_plural= "Registos em voluntariados"