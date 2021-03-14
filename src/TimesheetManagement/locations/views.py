from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Location

# Create your views here.
class LocationList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Location
    template_name = "locations/list.html"
    context_object_name = "locations"
    ordering = ["name", "sector"]
    extra_context = {"title": "List of Locations"}

    def test_func(self):
        return self.request.user.is_superuser


class LocationCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Location
    fields = ["name", "sector"]
    template_name = "locations/new_or_update.html"
    extra_context = {"title": "New Location"}

    def test_func(self):
        return self.request.user.is_superuser


class LocationUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Location
    fields = ["name", "sector"]
    template_name = "locations/new_or_update.html"
    extra_context = {"title": "Update Location"}

    def test_func(self):
        return self.request.user.is_superuser


class LocationDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Location
    template_name = "locations/delete.html"
    extra_context = {"title": "Delete Location"}
    success_url = reverse_lazy("locations:list")

    def test_func(self):
        return self.request.user.is_superuser