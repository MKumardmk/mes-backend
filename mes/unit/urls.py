from django.urls import path,re_path
from . import views

urlpatterns = [
    path('units/',views.UnitView.as_view(),name="units")
]
