from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Fron managers.py
from .managers import UserManager

# La clase AbstractBaseUser ya nos trae toda una base para la creacion del modemlo User
# De esta manera se crea un modelo User en django
class User(AbstractBaseUser, PermissionsMixin):
    """Model definition for User."""

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino')
    )

    username = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    nombres = models.CharField(max_length=30, blank=True)
    apellidos = models.CharField(max_length=30, blank=True)
    genero = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    cod_registro = models.CharField(max_length=6, blank=True)
    # Este campo booleano me indica si el usuario tiene o no permisos para acceder al adinistrador
    is_staff = models.BooleanField(default=False)
    # Este campo me indica si el usuario esta verificado o no(Es decir si el email es correto)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    # Conectamos nuestro modelo con nuestro manager
    objects = UserManager()

    def get_short_name(self):
        return self.username

    def get_full_name(self) -> str:
        return self.nombres + ' ' + self.apellidos

    class Meta:
        """Meta definition for User."""

        verbose_name = 'User'
        verbose_name_plural = 'Users'


