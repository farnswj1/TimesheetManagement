from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path("new/", views.UserCreate.as_view(), name="create"),
    path("doctors/", views.DoctorList.as_view(), name="doctor_list"),
    path("doctors/<int:pk>/", views.DoctorDetail.as_view(), name="doctor_detail"),
    path("doctors/<int:pk>/update/", views.DoctorUpdate.as_view(), name="doctor_update"),
    path("doctors/<int:pk>/delete/", views.DoctorDelete.as_view(), name="doctor_delete"),
    path("admins/", views.AdminList.as_view(), name="admin_list"),
    path("admins/<int:pk>/", views.AdminDetail.as_view(), name="admin_detail"),
    path("admins/<int:pk>/update/", views.AdminUpdate.as_view(), name="admin_update"),
    path("admins/<int:pk>/delete/", views.AdminDelete.as_view(), name="admin_delete"),
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