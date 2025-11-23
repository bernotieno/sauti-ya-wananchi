"""
URL configuration for Sauti ya Wananchi project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # Landing, about, contact pages
    path('dashboard/', include('dashboard.urls')),  # Public analytics dashboard
    path('complaints/', include('complaints.urls')),  # Complaint submission
    path('accounts/', include('accounts.urls')),  # Auth (login, register, profile)
    path('citizen/', include('citizen.urls')),  # Citizen dashboard
    path('admin-panel/', include('admin_panel.urls')),  # Admin panel dashboard
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# Admin site customization
admin.site.site_header = 'Sauti ya Wananchi Admin'
admin.site.site_title = 'Sauti ya Wananchi'
admin.site.index_title = 'Complaints Management'
