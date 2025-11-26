from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('verify/<uuid:complaint_id>/', views.verify_complaint, name='verify'),
    path('complaints/', views.complaints_list, name='complaints_list'),
    path('complaints/<uuid:complaint_id>/', views.complaint_detail, name='complaint_detail'),
    path('users/', views.users_list, name='users_list'),
]
