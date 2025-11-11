from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
import string


def generate_access_code():
    """Generate a unique 12-character alphanumeric access code"""
    return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))


def generate_ticket_number():
    """Generate ticket number in format TCK-YYYY-NNNN"""
    year = timezone.now().year
    last_ticket = Ticket.objects.filter(
        ticket_number__startswith=f'TCK-{year}'
    ).order_by('-created_at').first()
    
    if last_ticket:
        last_num = int(last_ticket.ticket_number.split('-')[-1])
        new_num = last_num + 1
    else:
        new_num = 1
    
    return f'TCK-{year}-{new_num:04d}'


class CustomUser(AbstractUser):
    """Custom user model with role-based access"""
    ROLE_CHOICES = [
        ('TECNICO', 'Técnico'),
        ('USUARIO', 'Usuario'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USUARIO')
    institutional_email = models.EmailField(unique=True)
    access_code = models.CharField(max_length=12, unique=True, default=generate_access_code)
    code_sent_count = models.IntegerField(default=0)
    is_code_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.institutional_email})"
    
    def regenerate_code(self):
        """Regenerate access code"""
        self.access_code = generate_access_code()
        self.code_sent_count = 0
        self.is_code_active = True
        self.save()
        return self.access_code


class Ticket(models.Model):
    """Ticket model for helpdesk system"""
    STATUS_CHOICES = [
        ('ABIERTO', 'Abierto'),
        ('EN_PROGRESO', 'En Progreso'),
        ('RECHAZADO', 'Rechazado'),
        ('CERRADO', 'Cerrado'),
        ('ARCHIVADO', 'Archivado'),
    ]
    
    PRIORITY_CHOICES = [
        ('ALTA', 'Alta'),
        ('MEDIA', 'Media'),
        ('BAJA', 'Baja'),
    ]
    
    CATEGORY_CHOICES = [
        ('COMPUTADORA', 'Computadora (PC)'),
        ('IMPRESORA', 'Impresora'),
        ('SOFTWARE', 'Aplicación/Software'),
        ('RED', 'Red/Conectividad'),
        ('ACCESO', 'Acceso/Cuenta'),
        ('OTRO', 'Otro'),
    ]
    
    ticket_number = models.CharField(max_length=20, unique=True, default=generate_ticket_number)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tickets')
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIA')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='ABIERTO')
    affected_equipment = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Scheduling
    visit_date = models.DateField(blank=True, null=True)
    visit_time = models.TimeField(blank=True, null=True)
    
    # Rejection/Closure
    rejection_reason = models.TextField(blank=True, null=True)
    closure_note = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.ticket_number} - {self.user.get_full_name()}"
    
    def get_short_description(self):
        """Return first 50 characters of description"""
        return self.description[:50] + '...' if len(self.description) > 50 else self.description


class TicketAttachment(models.Model):
    """Photo attachments for tickets"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='attachments')
    image = models.ImageField(upload_to='ticket_photos/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Attachment for {self.ticket.ticket_number}"


class TicketHistory(models.Model):
    """Audit trail for ticket changes"""
    ACTION_CHOICES = [
        ('CREATED', 'Creado'),
        ('STATUS_CHANGED', 'Estado Cambiado'),
        ('VISIT_SCHEDULED', 'Visita Programada'),
        ('REJECTED', 'Rechazado'),
        ('CLOSED', 'Cerrado'),
        ('NOTE_ADDED', 'Nota Agregada'),
        ('ARCHIVED', 'Archivado'),
    ]
    
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='history')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    comment = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Ticket histories'
    
    def __str__(self):
        return f"{self.ticket.ticket_number} - {self.get_action_display()} by {self.user}"


class Notification(models.Model):
    """In-app notifications for users"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"
