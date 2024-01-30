from django.urls import path,re_path
from . import views

from rest_framework.routers import DefaultRouter

router=DefaultRouter()


app_name = "plant"
urlpatterns = [
    path("time-zone/", view=views.time_zone_list, name="time_zone"),
    path("language/", view=views.language_list, name="language"),
    path("unit/", view=views.unit_list, name="unit"),
    path("currency/", view=views.currency_list, name="currency"),
    path("product/", view=views.product_list, name="product"),
    # path("function/", view=views.function_list, name="function"),
    path("function/", view=views.FunctionListView.as_view(), name="function"),
    # path("plant-config/", view=views.plant_config_get, name="plant_config"),
    # re_path(r'^plant-config/(?P<pk>\d+)?/?$',views.PlantConfigView.as_view(),name='plant_config'),
    path('plant-config/<str:pk>/',views.PlantConfigView.as_view(),name='plant_config'),
    path('plant-config-post/',views.PlantConfigView.as_view(),name='plant_config'),
    re_path(r'^furnace-config/(?P<pk>\d*)?/?$',views.FurnaceConfigView.as_view(),name='furnace_config'),
    # re_path(r'^furnace-config/(?P<plant_id>\d*)?/?(?P<pk>\d*)?/?$',views.FurnaceConfigView.as_view(),name='furnace_config'),
    re_path(r'^furnace-config-steps/(?P<furnace_id>\d*)?/?$', views.FurnaceConfigStepListAPIView.as_view(), name='furnace_config_steps_list'),

    #  furnace config change order
    path('furnace-config-change-order/',views.FurnaceConfigChangeOrder.as_view(),name="furnace_config_change_order"),
    # path('furnace-config-steps/<int:pk>/', views.FurnaceConfigStepDetailAPIView.as_view(), name='furnace_config_steps_detail'),
    path("furnace-config-deactivate/<int:pk>/",views.FurnaceDeactivateView.as_view(),name="furnace_deactivate"),
    #  re_path(r'^plant-config/(?P<pk>\d+)?/$', views.PlantConfigView.as_view(), name='plant_config'),
    path("plant-config-create/", view=views.plant_config, name="plant_config_add"),
    path("plant-config-update/", view=views.plant_config_update, name="plant_config_update"),
    path("erp/", view=views.erp_list, name="ERP"),
]
