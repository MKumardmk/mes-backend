"""
URL configuration for mes project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from .initial_data import CreateSuperUserView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',CreateSuperUserView.as_view(),name='create_initial_data'),
     path("api/account/", include("accounts.urls", namespace="account")),

     path("api/plant/", include("app.plant.urls", namespace="plant")),
     path("api/master/", include("app.master.urls", namespace="master")),
]
