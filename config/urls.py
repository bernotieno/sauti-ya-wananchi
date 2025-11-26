"""
URL configuration for Sauti ya Wananchi project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    """Health check endpoint for Railway and monitoring."""
    import os
    from django.db import connection

    status_data = {
        'status': 'healthy',
        'service': 'Sauti ya Wananchi',
        'version': '1.0.0',
        'environment': os.getenv('RAILWAY_ENVIRONMENT', 'unknown'),
    }

    # Try database connection
    try:
        connection.ensure_connection()
        status_data['database'] = 'connected'
    except Exception as e:
        status_data['database'] = f'error: {str(e)}'
        status_data['status'] = 'unhealthy'

    return JsonResponse(status_data)

urlpatterns = [
    path('health/', health_check, name='health_check'),  # Health check for Railway
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
