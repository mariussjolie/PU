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

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('auth/', include('WebApp.auth.urls')),
    path('estates/<int:estate_id>/', views.view_estate, name='estate'),
    path('estates/<int:estate_id>/adminoverview/', views.admin_view_estate, name='estate.adminoverview'),
    path('estates/<int:estate_id>/<int:item_id>/notify/<int:user_id>/', views.notify, name='user_notify'),
    # path('estates/<int:estate_id>/end_estate/', TemplateView.as_view(template_name='estate/end_estate.html'), name='end_estate'),
    path('estates/<int:estate_id>/<int:item_id>/addcomment', views.write_comment, name='estate_addcomment'),
    path('estates/<int:estate_id>/<int:item_id>/', views.show_item, name='show_item'),

    path('estates/<int:estate_id>/<int:item_id>/adminoverview', views.admin_view_item, name='admin_view_estate_item'),
    path('estate/<int:estate_id>/distribute', views.admin_estate_distribute, name='estate_notfinished'),
    path('estate/<int:estate_id>/distribute/<int:item_id>', views.estate_item_distribute, name='estate_item_finished'),
    path('estate/<int:estate_id>/finish', views.finish_estate, name='finish_estate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
