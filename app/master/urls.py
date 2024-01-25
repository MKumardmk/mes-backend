from django.urls import path
from . import views


app_name = "master"
urlpatterns = [
    # path("master/", view=master_list, name="master"),
    path("master/", view=views.MasterListView.as_view(), name="master_list"),

]
