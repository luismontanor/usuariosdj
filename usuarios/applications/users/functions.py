"""Funciones extra de la aplicación users"""

# Importación de paquetes necesarios
import random
import string

# Funcion que me permite generar un codigo aleatorio de longitud 6 que puede contener numeros y letras
def code_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))