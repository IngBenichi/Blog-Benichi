from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Comment

class BaseForm:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'w-full px-4 py-2 mt-1 text-sm border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent bg-white'
            field.widget.attrs['widget_container'] = 'div'
            field.widget.attrs['widget_container_attrs'] = {'class': 'flex flex-col space-y-1 mb-4'}

class EmailPostForm(BaseForm, forms.Form):
    name = forms.CharField(
        max_length=25,
        label='Nombre',
        widget=forms.TextInput(attrs={
            'placeholder': 'Tu nombre',
            'class': 'w-full px-4 py-2 mt-1 text-sm border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none bg-white'
        })
    )
    to = forms.EmailField(
        label='Destinatario',
        widget=forms.EmailInput(attrs={
            'placeholder': 'correo@ejemplo.com',
            'class': 'w-full px-4 py-2 mt-1 text-sm border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none bg-white'
        })
    )
    comments = forms.CharField(
        required=False,
        label='Comentarios',
        widget=forms.Textarea(attrs={
            'placeholder': 'Escribe tus comentarios aquí...',
            'rows': 4,
            'class': 'w-full px-4 py-2 mt-1 text-sm border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent outline-none bg-white resize-none'
        })
    )

class CommentForm(BaseForm, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Comentario'
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'placeholder': 'Escribe tu comentario aquí...',
                'rows': 6,
                'class': 'w-full px-4 py-2 mt-1 text-sm border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent focus:outline-none bg-white resize-none'
            })
        }

class SearchForm(BaseForm, forms.Form):
    query = forms.CharField(
        label='Búsqueda',
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar...',
            'class': 'w-full px-4 py-2 text-sm border rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent focus:outline-none bg-white'
        })
    )

class CustomLoginForm(BaseForm, AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Tu usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Tu contraseña'})
    )

class CustomRegisterForm(BaseForm, UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite la contraseña'})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
