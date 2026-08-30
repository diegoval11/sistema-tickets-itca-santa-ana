from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Ticket, TicketAttachment, TicketHistory, Notification


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'institutional_email', 'role', 'is_code_active', 'code_sent_count']
    list_filter = ['role', 'is_code_active']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'institutional_email'),
        }),
        ('Permisos y Rol', {
            'fields': ('role', 'is_staff', 'is_active'),
        }),
    )
    
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'institutional_email')
        }),
        ('Información de Acceso', {
            'fields': ('role', 'access_code', 'code_sent_count', 'is_code_active')
        }),
        ('Permisos', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'user', 'category', 'priority', 'status', 'created_at']
    list_filter = ['status', 'category', 'priority', 'created_at']
    search_fields = ['ticket_number', 'description', 'user__username']
    readonly_fields = ['ticket_number', 'created_at', 'updated_at']


@admin.register(TicketAttachment)
class TicketAttachmentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'uploaded_at']
    list_filter = ['uploaded_at']


@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'action', 'user', 'timestamp']
    list_filter = ['action', 'timestamp']
    readonly_fields = ['timestamp']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
