from mimetypes import init
from django import forms
# Importamos lo siguiente para poder realizar una autenticacion de usuario
from django.contrib.auth import authenticate

from .models import User


class UserRegisterForm(forms.ModelForm):
    """Form definition for UserRegisterForm."""

    #
    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
            }
        ),
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir contraseña',
            }
        ),
    )

    class Meta:
        """Meta definition for UserRegisterFormform."""

        model = User
        fields = (
            'username',
            'email',
            'nombres',
            'apellidos',
            'genero',
        )

    # Funcion para validar el password
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'No coinciden las contraseñas')
            self.add_error('password1', 'No coinciden las contraseñas')


# Se hereda del forms.Form cuando el formulario no depende de un model
class LoginForm(forms.Form):

    username = forms.CharField(
        label='Username',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Usuario',
            }
        ),
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
            }
        ),
    )

    # Se utiliza esta funcion para validacion de usuario y contraseña
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        # Recuperamos el usuario y la contraseña escritos
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            # Cortamos el proceso y mandamos un error
            raise forms.ValidationError('Los datos de usuarios no son correctos!')
        return self.cleaned_data


# Se hereda del forms.Form cuando el formulario no depende de un model
class UpdatePasswordForm(forms.Form):
    """Form definition for UpdatePassword."""

    current_password = forms.CharField(
        label='Contraseña actual:',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña actual',
            }
        ),
    )
    new_password = forms.CharField(
        label='Contraseña nueva:',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña nueva',
            }
        ),
    )


# Se hereda del forms.Form cuando el formulario no depende de un model
class VerificationForm(forms.Form):
    """Form definition for Verification."""

    # Sobreescribimos la funcion __init__ que es la que se ejecuta al iniciar el formulario
    def __init__(self, pk, *args, **kwargs):
        # Recuperamos el pk de la vista y la almacenamos en id_user
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    cod_registro = forms.CharField(label='Código de verificación', required=True)

    # Hacemos la validacion del codigo ingresado por el usuario y del que se tiene en la base de datos
    def clean_cod_registro(self):
        # Recuperamos el codigo de registro
        codigo = self.cleaned_data['cod_registro']

        # primero validamos que el codigo ingresado tenga la longitud adecuada(6)
        if len(codigo)==6:
            # Verificamos si el codigo y el id del usuario son validos
            activo = User.objects.cod_validator(
                # Recuperamos el id de la vista
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('El código es incorrecto!')
        else:
            # Enviamos un error de la siguiente forma
            # self.add_error('cod_registro')
            raise forms.ValidationError('El código es incorrecto!')
