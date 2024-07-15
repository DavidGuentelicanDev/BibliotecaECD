from sqlite3 import IntegrityError
from django import forms
from .models import Libro, Usuario, Reserva, DetalleReserva
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation


#FORMULARIOS PARA EL CRUD
#crear y editar libros
class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = '__all__'
        widgets = {
            'codigo': forms.NumberInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'subtitulo': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'resena': forms.Textarea(attrs={'class': 'form-control'}),
            'editorial': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'portada': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'estado_libro': forms.Select(attrs={'class': 'form-select'}),
        }
        labels = {'resena': 'Reseña'}

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if self.instance.pk is None and Libro.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("El código ingresado ya está registrado.")
        elif self.instance.pk is not None and self.instance.codigo != codigo and Libro.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("El código ingresado ya está registrado.")
        return codigo
    
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if self.instance.pk is None and Libro.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError("El título ingresado ya está registrado.")
        elif self.instance.pk is not None and self.instance.titulo != titulo and Libro.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError("El título ingresado ya está registrado.")
        return titulo

#crear y editar usuario cliente (no se podran crear usuarios administradores ni superusuarios)
class UsuarioForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Su contraseña no puede asemejarse tanto a su otra información personal.\nDebe contener al menos 8 caracteres.\nNo puede ser una clave utilizada comúnmente.\nSu contraseña no puede ser completamente numérica.'
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Repita la contraseña para verificar.'
    )

    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'rut',
            'email',
            'username',
            'telefono',
            'direccion',
            'comuna',
            'password1',
            'password2'
        ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        help_texts = {'username': 'Debe tener formato de correo electrónico.',}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if self.instance.pk is None and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if self.instance.pk is None and Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya está en uso.')
        return username

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if self.instance.pk is None and Usuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este rut ya está registrado.')
        return rut

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data

#RESERVA
#crear y editar reservas
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['usuario']
        widgets = {'usuario': forms.Select(attrs={'class': 'form-select'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = Usuario.objects.filter(is_staff=False) #filtrar usuarios que no sean staff

#agregar libro a la reserva
class AgregarLibroForm(forms.ModelForm):
    class Meta:
        model = DetalleReserva
        fields = ['libro']
        widgets = {'libro': forms.Select(attrs={'class': 'form-select'})}

    def __init__(self, reserva=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reserva = reserva
        libros = Libro.objects.all()
        choices = [
            (libro.codigo, f"{libro.titulo} - {'NO DISPONIBLE' if libro.estado_libro != 'D' else 'Disponible'}")
            for libro in libros
        ]
        self.fields['libro'].choices = choices

    def clean_libro(self):
        libro = self.cleaned_data.get('libro')
        if libro.estado_libro != 'D':
            raise forms.ValidationError('El libro seleccionado no está disponible.')
        return libro

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.reserva:
            instance.reserva = self.reserva
        if commit:
            instance.save()
        return instance


#USUARIOS
#formulario para el registro de cliente
class RegistroForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Su contraseña no puede asemejarse tanto a su otra información personal.\nDebe contener al menos 8 caracteres.\nNo puede ser una clave utilizada comúnmente.\nSu contraseña no puede ser completamente numérica.'
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Repita la contraseña para verificar.'
    )

    class Meta:
        model = Usuario
        fields = [
            'first_name',
            'last_name',
            'rut',
            'username',
            'telefono',
            'direccion',
            'comuna',
            'password1',
            'password2'
        ]
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        help_texts = {'username': '',}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado como usuario.')
        return username
    
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if Usuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError('Este rut ya está registrado.')
        return rut
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.username #el campo email se guardara igual al campo username
        if commit:
            user.save()
        return user

#formulario para perfil (cliente)
class PerfilForm(UserChangeForm):
    password = None #excluir campo de password

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rut', 'username', 'telefono', 'direccion', 'comuna']
        labels = {
            'first_name': 'Nombres',
            'last_name': 'Apellidos',
            'username': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
        }
        help_texts = {'username': '',}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'comuna': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if Usuario.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado como usuario.')
        return username
    
    def clean_rut(self):
        rut = self.cleaned_data['rut']
        if Usuario.objects.filter(rut=rut).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Este rut ya está registrado.')
        return rut
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['username']
        if commit:
            try:
                user.save()
            except IntegrityError as e:
                raise forms.ValidationError('Hubo un problema al actualizar el perfil.')
        return user

#formulario para actualizar password
class CambiarPasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Ingrese su contraseña actual.'
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Debe contener al menos 8 caracteres.'
    )
    new_password2 = forms.CharField(
        label="Confirmar nueva contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        help_text='Repita la nueva contraseña para verificar.'
    )

    class Meta:
        model = Usuario
        fields = ['old_password', 'new_password1', 'new_password2']
