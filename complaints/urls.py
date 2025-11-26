from django.urls import path
from . import views

app_name = 'complaints'

urlpatterns = [
    path('submit/', views.ComplaintCreateView.as_view(), name='submit'),
    path('submit/anonymous/', views.AnonymousComplaintCreateView.as_view(), name='submit_anonymous'),
    path('success/', views.complaint_success, name='success'),
    path('<uuid:pk>/', views.ComplaintDetailView.as_view(), name='detail'),
    path('<uuid:pk>/card/', views.complaint_card, name='card'),
]
