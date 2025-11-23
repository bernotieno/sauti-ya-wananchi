from django.urls import path
from . import views

app_name = 'citizen'

urlpatterns = [
    path('dashboard/', views.citizen_dashboard, name='dashboard'),
]
