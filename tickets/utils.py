from django.core.mail import send_mail
from django.conf import settings
from .models import Notification


def send_ticket_notification(ticket, title, message, recipient_user):
    """
    Send notification to user via email and in-app
    """
    # Create in-app notification
    Notification.objects.create(
        user=recipient_user,
        ticket=ticket,
        title=title,
        message=message
    )
    
    # Send email
    send_mail(
        subject=f'{title} - Ticket {ticket.ticket_number}',
        message=f'Hola {recipient_user.get_full_name()},\n\n{message}\n\nNúmero de Ticket: {ticket.ticket_number}\n\nPuedes ver más detalles en el sistema.\n\nSaludos,\nEquipo de Soporte Técnico ITCA FEPADE',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[recipient_user.institutional_email],
        fail_silently=True,
    )


def send_bulk_notification(title, message, users):
    """
    Send notification to multiple users
    """
    for user in users:
        Notification.objects.create(
            user=user,
            title=title,
            message=message
        )
        
        send_mail(
            subject=title,
            message=f'Hola {user.get_full_name()},\n\n{message}\n\nSaludos,\nEquipo de Soporte Técnico ITCA FEPADE',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.institutional_email],
            fail_silently=True,
        )
