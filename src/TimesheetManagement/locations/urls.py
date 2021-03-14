from django.urls import path
from . import views

app_name = "locations"

urlpatterns = [
    path("", views.LocationList.as_view(), name="list"),
    path("new/", views.LocationCreate.as_view(), name="create"),
    path("<int:pk>/update/", views.LocationUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.LocationDelete.as_view(), name="delete"),
]