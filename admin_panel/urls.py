from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('verify/<uuid:complaint_id>/', views.verify_complaint, name='verify'),
]
