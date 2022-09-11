import datetime
from django.shortcuts import render
# Importamos esta clase para utilizarla en el inicio de sesion
# Con esta clase vamos a lograr hacer una autenticacion en cada una de
# las vistas que se requiere haber iniciado sesion para poderlas mostrar
from django.contrib.auth.mixins import LoginRequiredMixin
# Se usa reverse_lazy para gestionar urls en django
from django.urls import reverse_lazy

from django.views.generic import (
    TemplateView
)


# Construccion de un mixin
class FechaMixin(object):

    # Esta funcion se usa siempre que se quiera enviar un contexto al template
    def get_context_data(self, **kwargs):
        context = super(FechaMixin, self).get_context_data(**kwargs)
        # Creamos un contexto fecha
        context['fecha'] = datetime.datetime.now()
        return context


# Se usa LoginRequiredMixin hacer una autenticacion en cada una de las
# vistas que se requiere haber iniciado sesion para poderlas mostrar
class HomePage(LoginRequiredMixin, TemplateView):
    template_name = "home/index.html"
    # El LoginRequiredMixin requiere de un atributo necesario
    # La cual va a decir que va a suceder cuando intenten acceder a la vista sin haber iniciado sesion
    # En este caso vamos a redireccionar a la vista user_login
    login_url = reverse_lazy('users_app:user_login')


class TemplatePruebaMixin(FechaMixin, TemplateView):
    template_name = "home/mixin.html"
