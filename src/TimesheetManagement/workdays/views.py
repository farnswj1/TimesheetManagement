from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import WorkDay
from .forms import WorkDayForm
from django.contrib.auth.models import User

# Create your views here.
class WorkDayList(LoginRequiredMixin, ListView):
    model = WorkDay
    template_name = "workdays/list.html"
    context_object_name = "workdays"
    ordering = ["work_date"]
    extra_context = {"title": "List of Work Days"}
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            first_name = self.request.GET.get("first_name")
            last_name = self.request.GET.get("last_name")
            
            if first_name and last_name:
                user_ = User.objects.filter(
                    first_name__icontains=first_name.strip(),
                    last_name__icontains=last_name.strip()
                )
            elif first_name:
                user_ = User.objects.filter(first_name__icontains=first_name.strip())
            elif last_name:
                user_ = User.objects.filter(last_name__icontains=last_name.strip())
            else:
                user_ = User.objects.none()

            if user_:
                return WorkDay.objects.filter(user=user_[0]).order_by("work_date", "time_in")
            else:
                return WorkDay.objects.none()
        else:
            return WorkDay.objects.filter(user=self.request.user).order_by("work_date", "time_in")
            

class WorkDayCreate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    model = WorkDay
    template_name = "workdays/new_or_update.html"
    extra_context = {"title": "New Work Day"}
    form_class = WorkDayForm
    success_message = "Workday was successfully created!"

    def test_func(self):
        return self.request.user.is_superuser


class WorkDayDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = WorkDay
    template_name = "workdays/detail.html"
    context_object_name = "workday"
    extra_context = {"title": "Work Day Information"}

    def test_func(self):
        return self.request.user.is_superuser or self.get_object().user == self.request.user


class WorkDayUpdate(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = WorkDay
    template_name = "workdays/new_or_update.html"
    extra_context = {"title": "Update Work Day"}
    form_class = WorkDayForm
    success_message = "Workday was successfully updated!"

    def test_func(self):
        return self.request.user.is_superuser and not self.get_object().is_locked()


class WorkDayDelete(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = WorkDay
    template_name = "workdays/delete.html"
    extra_context = {"title": "Delete Work Day"}
    success_url = reverse_lazy("workdays:list")
    success_message = "Workday was successfully deleted!"

    def test_func(self):
        return self.request.user.is_superuser and not self.get_object().is_locked()