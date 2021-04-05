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
    path('', views.home, name='home'),
    path('auth/', include('WebApp.auth.urls')),
    path('estates/<int:estate_id>/', views.view_estate, name='estate'),
    path('estates/<int:estate_id>/adminoverview/', views.admin_view_estate, name='estate.adminoverview'),
    path('estates/<int:estate_id>/<int:item_id>/notify/<int:user_id>/', views.notify, name='user_notify'),
    path('estates/<int:estate_id>/end_estate/', TemplateView.as_view(template_name='estate/end_estate.html'), name='end_estate'),
    path('status/<int:estate_id>/', views.status, name='status'),
    path('estates/<int:estate_id>/<int:item_id>/addcomment', views.write_comment, name='estate_addcomment'),
    path('estates/<int:estate_id>/<int:item_id>/', views.show_item, name='show_item'),

    path('estates/<int:estate_id>/<int:item_id>/adminoverview', views.admin_view_item, name='admin_view_estate_item'),
    path('estate_notfinished/<int:estate_id>/', views.admin_estate_notfinished, name='estate_notfinished'),
    path('estate_item_finished/<int:estate_id>/<int:item_id>/', views.estate_item_finished, name='estate_item_finished'),
    path('estate_finished/<int:estate_id>/', views.finish_estate, name='finish_estate'),

    # Front-end-skisser:

    path('frontend/4', TemplateView.as_view(template_name='WebApp/estate/estate_admin_notfinished.html'), name='estate_notfinished'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
