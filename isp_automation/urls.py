# isp_automation/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # For initial redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='login/', permanent=False)), # Redirect root to login
    path('users/', include('users.urls')), # User authentication URLs
    path('app/', include('core.urls')),    # Core application URLs
    # Add other URL patterns as needed
]
