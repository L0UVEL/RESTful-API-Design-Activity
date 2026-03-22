"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from api.frontend_views import admin_dashboard, admin_user_management, custom_login, custom_logout, admin_appointments, student_dashboard
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    # Replace default admin login with ours, or just add a new route
    path('admin/login/', custom_login, name='custom-login'),
    path('login/', custom_login, name='custom-login-base'),
    path('logout/', custom_logout, name='custom-logout'),
    
    # Custom Admin Frontend Routes
    # THESE MUST COME BEFORE path('admin/', admin.site.urls)
    path('admin/users/add', admin_user_management, name='admin-user-management'),
    path('admin/appointments', admin_appointments, name='admin-appointments'),
    
    # Default Django Admin
    path('admin/', admin.site.urls),
    
    path('api/', include('api.urls')),
    
    # Other Frontend Routes
    path('admin-dashboard', admin_dashboard, name='admin-dashboard'),
    path('student-dashboard', student_dashboard, name='student-dashboard'),

    # API Documentation
    path('api/schema', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
