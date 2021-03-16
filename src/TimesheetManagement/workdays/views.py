from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from .models import WorkDay
from .forms import WorkDayForm
from django.contrib.auth.models import User
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import datetime, date, timedelta
import calendar

# Create your views here.
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

class WorkDayList(LoginRequiredMixin, ListView):
    model = WorkDay
    template_name = "workdays/list.html"
    context_object_name = "workdays"
    ordering = ["work_date"]
    extra_context = {"title": "List of Work Days"}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(query=context["workdays"], withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        if context.get("workdays"):
            context["user_full_name"] = context["workdays"][0].user.full_name
        return context
    
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