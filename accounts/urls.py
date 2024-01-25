from django.urls import path,re_path

from . import views

app_name="accounts"
urlpatterns = [
    path('simple-login/',view=views.SimpleUserLoginView.as_view(),name="simple_login"),
    path('sso-login/',view=views.SSOLoginView.as_view(),name="sso_login"),
    re_path(r'^manage-role/',views.RolesView.as_view(),name="manage_roles"),
    path("clone_role/", view=views.clone_role, name="clone_role"),
    path("deactivate_role/", view=views.deactivate_role, name="deactivate_role"),


]
