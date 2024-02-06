from django.contrib import admin
from django.urls import path,include
from .initial_data import CreateSuperUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/account/", include("mes.users.urls", namespace="users")),
    path("api/master/", include("mes.utils.urls", namespace="master")),
     path("api/plant/", include("mes.plant.urls", namespace="plant")),
     path("api/furnace/", include("mes.plant.urls", namespace="plant")),
     path('api/',include('config.api_router'),),

    path('',CreateSuperUserView.as_view(),name='create_initial_data'),

]
