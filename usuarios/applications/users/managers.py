from django.db import models

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):

    # El campo is_staff indica si el nuevo usuarion puede o no ingresar al administrador de django
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active,**extra_fields):
        user = self.model(
            username = username,
            email = email,
            is_staff = is_staff,
            is_superuser = is_superuser,
            is_active = is_active,
            **extra_fields,
        )

        # Funcion para encriptar el password de un usuario
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, False, **extra_fields)

    # Funcion privada para la creacion de un superusuario
    def create_superuser(self, username, email, password=None, **extra_fields):
        return self._create_user(username, email, password, True, True, True, **extra_fields)

    # Manager para realizar la validacion de si coincide o no el codigo ingresado
    # con el codigo generado en el modelo
    # Y si le pertenece o no a dicha persona
    # En esta funcion indicamos ademas del self dos campos
    # el id y el codigo que recuperamos desde el formulario
    # y luego procedemos a realizar la validacion
    def cod_validator(self, id_user, validation_cod_registro):
        if self.filter(id=id_user, cod_registro=validation_cod_registro).exists():
            # En caso de que todo sea valido retortnamos True
            return True
        else:
            return False