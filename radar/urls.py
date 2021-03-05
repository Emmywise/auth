"""radar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import (
    RegisterView, LoginAPIView, LogoutAPIView, verifyEmail,
)


schema_view = get_schema_view(
    openapi.Info(
        title='RADAR API',
        default_version='v1',
        description='Test description',
        term_of_service="https//radar.com",
        contact=openapi.Contact(email='adefila.emmywise@gmail.com'),
        license=openapi.License(name='Test License'),
    ),

    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui',),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc',),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('verification/', include('verify_email.urls')),
    path('api/user-accounts/', RegisterView.as_view(), name='register'),
    path('api/user-login/', LoginAPIView.as_view(), name='login'),
    path('api/user-logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/email-verify', verifyEmail.as_view(), name='email-verify'),
]
