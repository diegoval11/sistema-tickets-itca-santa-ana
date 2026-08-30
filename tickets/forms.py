from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Ticket, TicketAttachment
from django.conf import settings


class AccessCodeLoginForm(forms.Form):
    """Login form using institutional email and access code"""
    institutional_email = forms.EmailField(
        label='Correo Institucional',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
            'placeholder': 'correo@itcafepade.edu.sv'
        })
    )
    access_code = forms.CharField(
        label='Código de Acceso',
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
            'placeholder': 'Ingrese su código'
        })
    )
    remember_me = forms.BooleanField(
        label='Recuérdame',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-primary bg-neutral-800 border-neutral-700 rounded focus:ring-primary'
        })
    )


class UserCreationFormByTechnician(forms.ModelForm):
    """Form for technician to create new users"""
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'institutional_email', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Apellido'
            }),
            'institutional_email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'correo@itcafepade.edu.sv'
            }),
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'nombre.usuario'
            }),
        }


class TicketCreationForm(forms.ModelForm):
    """Form for users to create tickets"""
    
    class Meta:
        model = Ticket
        fields = ['description', 'category', 'priority', 'affected_equipment', 'serial_number']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Describa el problema detalladamente...',
                'rows': 5
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100'
            }),
            'priority': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100'
            }),
            'affected_equipment': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Ej: PC Aula 12, Portátil del profesor X'
            }),
            'serial_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Número de serie (opcional)'
            }),
        }


class TicketUpdateForm(forms.ModelForm):
    """Form for technician to update ticket status"""
    class Meta:
        model = Ticket
        fields = ['status', 'visit_date', 'visit_time', 'rejection_reason', 'closure_note']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100'
            }),
            'visit_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100'
            }),
            'visit_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100'
            }),
            'rejection_reason': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Motivo del rechazo...',
                'rows': 3
            }),
            'closure_note': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-neutral-800 border border-neutral-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-neutral-100',
                'placeholder': 'Nota de cierre...',
                'rows': 3
            }),
        }
