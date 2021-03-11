from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("", views.UserList.as_view(), name="user_list"),
    path("<int:pk>/", views.UserDetail.as_view(), name="user_detail"),
    path("<int:pk>/update/", views.UserUpdate.as_view(), name="user_update"),
    path("<int:pk>/delete/", views.UserDelete.as_view(), name="user_delete"),
    path(
        "login/", 
        auth_views.LoginView.as_view(
            template_name="users/login.html", 
            extra_context={"title": "Login"}
        ), 
        name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]