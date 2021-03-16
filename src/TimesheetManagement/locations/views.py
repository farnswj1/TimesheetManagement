from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, FormView
from django.contrib.messages.views import SuccessMessageMixin
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
        
    def get_queryset(self):
        query = self.request.GET.get("search")
        if query:
            return Location.objects.filter(name__icontains=query.strip())
        else:
            return super().get_queryset()

class LocationCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = Location
    fields = ["name", "sector"]
    template_name = "locations/new_or_update.html"
    extra_context = {"title": "New Location"}
    success_message = "Location was successfully created!"

    def test_func(self):
        return self.request.user.is_superuser


class LocationUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = Location
    fields = ["name", "sector"]
    template_name = "locations/new_or_update.html"
    extra_context = {"title": "Update Location"}
    success_message = "Location was successfully updated!"

    def test_func(self):
        return self.request.user.is_superuser and not self.get_object().is_locked()


class LocationDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Location
    template_name = "locations/delete.html"
    extra_context = {"title": "Delete Location"}
    success_url = reverse_lazy("locations:list")
    success_message = "Location was successfully deleted!"

    def test_func(self):
        return self.request.user.is_superuser and not self.get_object().is_locked()
