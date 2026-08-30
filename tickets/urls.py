from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User views
    path('tickets/', views.my_tickets, name='my_tickets'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    
    # Technician views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.user_management, name='user_management'),
    path('users/create/', views.create_user, name='create_user'),
    path('users/<int:user_id>/resend-code/', views.resend_code, name='resend_code'),
    path('users/<int:user_id>/regenerate-code/', views.regenerate_code, name='regenerate_code'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<int:notification_id>/mark-read/', views.mark_notification_read, name='mark_notification_read'),
    
    # Export
    path('export/', views.export_tickets, name='export_tickets'),
]
