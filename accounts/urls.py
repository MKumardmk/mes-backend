from django.urls import path,re_path,include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register(r'functions', views.FunctionViewSet, basename='function')
app_name="accounts"
urlpatterns = [
    path('', include(router.urls)),
    path('simple-login/',view=views.SimpleUserLoginView.as_view(),name="simple_login"),
    path('sso-login/',view=views.SSOLoginView.as_view(),name="sso_login"),
    re_path(r'^roles/',views.RolesView.as_view(),name="manage_roles"),
    re_path(r'users/(?P<pk>\d+)?/?$',views.UserView.as_view(),name="user_view"),
    re_path(r'users-deactivate/(?P<pk>\d+)?/?$',views.DeactivateUser.as_view(),name="deactivate_user"),
    path("clone_role/", view=views.clone_role, name="clone_role"),
    path("deactivate_role/", view=views.deactivate_role, name="deactivate_role"),

    path('get-roles/',views.get_roles,name='get_roles'),
    

    # path('create-user/',views.CreateUserView.as_view(),name="create_user_view")


]
