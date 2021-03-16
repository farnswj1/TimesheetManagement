from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("", views.Report.as_view(), name="report"),
    path("export/<str:query>/", views.export, name="export"),
]