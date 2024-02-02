from django.urls import path,re_path
from . import views


urlpatterns = [
    re_path(r'^furnace-config/(?P<pk>\d*)?/?$',views.FurnaceConfigView.as_view(),name='furnace_config'),
    # re_path(r'^furnace-config/(?P<plant_id>\d*)?/?(?P<pk>\d*)?/?$',views.FurnaceConfigView.as_view(),name='furnace_config'),
    re_path(r'^furnace-config-steps/(?P<furnace_id>\d*)?/?$', views.FurnaceConfigStepListAPIView.as_view(), name='furnace_config_steps_list'),

    #  furnace config change order
    path('furnace-config-change-order/',views.FurnaceConfigChangeOrder.as_view(),name="furnace_config_change_order"),
    # path('furnace-config-steps/<int:pk>/', views.FurnaceConfigStepDetailAPIView.as_view(), name='furnace_config_steps_detail'),
    path("furnace-config-deactivate/<int:pk>/",views.FurnaceDeactivateView.as_view(),name="furnace_deactivate"),
]
