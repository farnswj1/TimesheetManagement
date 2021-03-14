from django.urls import path
from . import views

app_name = "workdays"

urlpatterns = [
    path("", views.WorkDayList.as_view(), name="list"),
    path("new/", views.WorkDayCreate.as_view(), name="create"),
    path("<int:pk>/", views.WorkDayDetail.as_view(), name="detail"),
    path("<int:pk>/update/", views.WorkDayUpdate.as_view(), name="update"),
    path("<int:pk>/delete/", views.WorkDayDelete.as_view(), name="delete"),
]