# pylint: skip-file
"""Røddi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangop/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home , name='home'),
    path('auth/', include('WebApp.auth.urls')),
    path('DB/', views.test_db, name='DB'),
    path('estates/', views.estate_overview, name='Estates'),
    path('estates/<int:estate_id>/', views.view_estate, name='estate'),
    path('estates/<int:estate_id>/end_estate/', TemplateView.as_view(template_name='estate/end_estate.html'), name='end_estate'),
    path('image_upload', views.item_image, name='image_upload'),
    path('success', views.success, name='success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
