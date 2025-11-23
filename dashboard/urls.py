from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('api/analytics/', views.analytics_api, name='analytics_api'),
]
