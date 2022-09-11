from django.shortcuts import render
# Importamos esta funcion que nos va a permitir enviar un email parta verificacion en los regiostros de usuario
from django.core.mail import send_mail
# Importamos esta clase para utilizarla en el inicio de sesion
# con esta clase vamos a lograr hacer una autenticacion en cada una de
# las vistas que se requiere haber iniciado sesion para poderlas mostrar
from django.contrib.auth.mixins import LoginRequiredMixin
# Estos modulos no permiten navegar mas facilmente entre las aplicaciones de nuestro sistema
from django.urls import reverse_lazy, reverse
# Importamos lo siguiente para poder realizar una autenticacion de usuario
from django.contrib.auth import (
    authenticate,
    login,
    logout
)
# Importamos lo siguiente para hacer una redireccion (En el logout en este caso)
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.views.generic import (
    View
)
# From forms
from .forms import (
    UserRegisterForm,
    LoginForm,
    UpdatePasswordForm,
    VerificationForm
)
# From models
from .models import User
#
from .functions import code_generator


class UserRegisterView(FormView):
    #model = User
    template_name = "users/register.html"
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        #
        # Generamos el codigo
        codigo = code_generator()

        new_user = User.objects.create_user(
            # Capturamos los parametros ingresados en los campos
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
                # Extra fields
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            cod_registro = codigo
        )
        # Enviar el codigo al email del nuevo usuario
        # De esta manera hacemos el respectivo envio de email para verificacion de las cuentas de usuarios
        asunto = 'Confirmación de email'
        mensaje = 'Código de verificación: ' + codigo
        email_remitent = 'luis.montano.rivera@utelvt.edu.ec'
        #
        send_mail(asunto, mensaje, email_remitent, [form.cleaned_data['email'],])

        # Redireccionamos a otra pantalla de validacion para hacer la confirmacion
        return HttpResponseRedirect(
            reverse(
                'users_app:user_verification',
                kwargs={'pk': new_user.id}
            )
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:panel')

    # Luego de haber importado authenticate procedemos a hacer la validacion
    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)


# Funcion para cherrar sesion
# Heredamos del View
class LogOutView(View):

    # Interceptamos la funcion get de la siguiente manera
    def get(self, request, **args):
        logout(request)

        # Redireccionamos a otra pantalla luego de hacer el logout
        return HttpResponseRedirect(
            reverse('users_app:user_login')
        )


# Vista para actualizar contraseña de un usuario
# Se usa LoginRequiredMixin hacer una autenticacion en cada una de las
# vistas que se requiere haber iniciado sesion para poderlas mostrar
class UpdatePassword(LoginRequiredMixin, FormView):

    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user_login')
    # El LoginRequiredMixin requiere de un atributo necesario
    # La cual va a decir que va a suceder cuando intenten acceder a la vista sin haber iniciado sesion
    # En este caso vamos a redireccionar a la vista user_login
    login_url = reverse_lazy('users_app:user_login')

    # Realizamos el proceso de actualizacion de contraseña
    def form_valid(self, form):
        # Recuperamos los datos del usuario que esta en sesion activa
        active_user = self.request.user

        # Realizamos una autenticacion del usuario que esta activo
        user = authenticate(
            username = active_user.username,
            password = form.cleaned_data['current_password']
        )

        # Realizamos el cambio de contraseña
        if user:
            # Recuperamos la nueva contraseña desde el formulario y la asignamos a una nmueva variable
            new_password = form.cleaned_data['new_password']
            # De esta manera obtenemos el campo password de nuestro modelo y le asignamos la nueva contraseña
            active_user.set_password(new_password)
            # Guardamos todo los cambios
            active_user.save()

        # Realizamos un cierre de sesion para que el usuario pruebe su nueva contraseña para acceder al sistema
        logout(self.request)
        return super(UpdatePassword, self).form_valid(form)

# Vista para hacer una verificacion del codigo enviado para
# la confirmacion de cuenta mediante correo electronico
class CodeVerificationView(FormView):
    template_name = 'users/verification.html'
    form_class = VerificationForm
    success_url = reverse_lazy('users_app:user_login')


    # Sobreescribimos la siguiente funcion
    def get_form_kwargs(self):
        kwargs = super(CodeVerificationView, self).get_form_kwargs()
        # Actualizamos los kwargs con algun valor para que lo pueda leer nuestro formulario
        kwargs.update({
            # Con esto le decimos a la vista que envie nuevos kwargs al formulario
            'pk': self.kwargs['pk'],
        })
        return kwargs

    def form_valid(self, form):
        # Actualizamos el valor
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            # Una vez verificado el usuario le concedemos los permisos
            is_active=True
        )
        return super(CodeVerificationView, self).form_valid(form)