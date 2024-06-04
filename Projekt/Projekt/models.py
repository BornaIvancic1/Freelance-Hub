from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser, Group, Permission
from django.db import models
def is_freelancer(user):
    return user.groups.filter(name='Freelancer').exists()
def is_tvrtka(user):
    return user.groups.filter(name='Tvrtka').exists()
class KorisnikManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        """
       
        """
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        username = extra_fields.pop('username', '')
        first_name = extra_fields.pop('first_name', '')  
        last_name = extra_fields.pop('last_name', '') 

        user = self.model(email=email, username=username, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Korisnik(AbstractUser):
 
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

 
    email = models.EmailField(unique=True)  
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    objects = KorisnikManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.password:
         self.set_password(self.password)
        return super().save(*args, **kwargs)

class Tvrtka(models.Model):
    user = models.OneToOneField(Korisnik, on_delete=models.CASCADE)

    @staticmethod
    def create_tvrtka(user):
        if user.is_superuser:
            tvrtka = Tvrtka.objects.create(user=user)
            return tvrtka

    def create_tvrtka_user(self, email, password, first_name, last_name,username):
        tvrtka_user = Korisnik.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        tvrtka = Tvrtka.create_admin(tvrtka_user)
        return tvrtka

   


class Freelancer(models.Model):
    user = models.OneToOneField(Korisnik, on_delete=models.CASCADE)
    

    @staticmethod
    def create_freelancer(user):
        freelancer = Freelancer.objects.create(user=user)
        return freelancer
def create_freelancer(self, email, password, first_name, last_name,username):
        freelancer_user = Korisnik.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, username=username)
        freelancer = Freelancer.create_freelancer(freelancer_user)
        return freelancer
def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Posao(models.Model):
    naziv_posla = models.CharField(max_length=255)

    def __str__(self):
        return self.naziv_posla

    class Meta:
        verbose_name_plural = "Poslovi"

class ObjavaPosla(models.Model):
    naslov = models.CharField(max_length=255)
    sadrzaj = models.TextField()
    datum_objave = models.DateField()
    datum_isteka = models.DateField()
    posao = models.ForeignKey(Posao, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.naslov

    class Meta:
        verbose_name_plural = "ObjavePosla"
