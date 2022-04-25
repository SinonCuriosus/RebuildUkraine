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
    date_joined                 =models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login                  =models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin                    =models.BooleanField(default=False)
    is_active                   = models.BooleanField(default=True)
    is_staff                    = models.BooleanField(default=False)
    is_superuser                = models.BooleanField(default=False)
    is_person                   = models.BooleanField(default=True)
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

    class Meta:
        abstract = False
        verbose_name= "Utilizadores singulares"
        verbose_name_plural= "Utilizadores singulares"


class MyEnterpriseManager(BaseUserManager):
    # Se adicionar nos REQUIRED arguments do USER mais argumentos, tenho que acrescentar aqui também
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have an username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Enterprise(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    taxnumber = models.CharField(max_length=9, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_enterpise = models.BooleanField(default=True)
    address = models.CharField(max_length=150)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    objects = MyEnterpriseManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


#Poderemos acrescentar mais países através do tuplo!
class Country(models.Model):
    UKRAINI='Ucrânia'
    COUNTRIES = [
        (UKRAINI,'Ucrânia'),
    ]
    country                     =models.CharField(max_length=25,choices=COUNTRIES)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name= "País"
        verbose_name_plural= "Países"



class City(models.Model):
    KIEV='Kiev'
    KHARKIV='Kharkiv'
    MARIUPOL='Mariupol'
    CITIES = [
        (KIEV,'Kiev'),
        (KHARKIV,'Kharkiv'),
        (MARIUPOL,'Mariupol'),
    ]
    country                     =models.ForeignKey(Country, on_delete=models.CASCADE)
    city                        =models.CharField(max_length=25,choices=CITIES)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name= "Cidade"
        verbose_name_plural= "Cidades"


class Expertise(models.Model):
    expertiseSubject            =models.CharField(max_length=250)

    def __str__(self):
        return self.expertiseSubject

    class Meta:
        verbose_name= "Especialização"
        verbose_name_plural= "Especializações"

class Specialization(models.Model):
    expertise                   =models.ManyToManyField(Expertise)
    person                      =models.ManyToManyField(Person)

    def __str__(self):
        return self.pk

    class Meta:

        verbose_name= "Voluntário especialista"
        verbose_name_plural= "Voluntários especializados"

#Rever se acham que vale a pena só a cidade
class Proposal(models.Model):
    enterprise                  =models.OneToOneField(Enterprise,on_delete=models.CASCADE)
    city                        =models.ForeignKey(City, on_delete=models.CASCADE)
    expertiseNeeded             =models.OneToOneField(Expertise,on_delete=models.CASCADE)
    description                 =models.CharField(max_length=150)

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name= "Proposta de voluntariado"
        verbose_name_plural= "Propostas de voluntariado"

class Favorites(models.Model):
    person                      =models.ManyToManyField(Person)
    proposal                    =models.ManyToManyField(Proposal)

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name= "Favorito"
        verbose_name_plural= "Favoritos"

class Registration(models.Model):
    person                      =models.ManyToManyField(Person)
    proposal                    =models.ManyToManyField(Proposal)

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name= "Registo em voluntariado"
        verbose_name_plural= "Registos em voluntariados"