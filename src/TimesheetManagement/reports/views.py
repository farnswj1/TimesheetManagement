import csv
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from workdays.models import WorkDay
from django.utils.timezone import now
from datetime import datetime, timedelta
from .forms import DateRangeForm


# Create your views here.
def export(request, query):
    query = tuple(map(int, query.split()))
    
    workdays = WorkDay.objects.filter(
        work_date__gte=datetime(query[2], query[0], query[1]),
        work_date__lte=datetime(query[5], query[3], query[4])
    )
    
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(
        ["work_date", "file_number", "employee_name", "time_in", 
        "time_out", "hours_worked", "location", "sector", 
        "hours_code", "fbp_payroll", "amco_payroll"
    ])
    
    for workday in workdays:
        writer.writerow([
            workday.work_date,
            workday.user.id,
            workday.user.full_name(),
            workday.time_in,
            workday.time_out,
            workday.hours_worked(),
            workday.location.name,
            workday.location.sector,
            workday.hours_code,
            workday.fbp_payroll,
            workday.amco_payroll
        ])

    return response


class Report(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = WorkDay
    template_name = "reports/report.html"
    context_object_name = "workdays"
    extra_context = {"title": "Reports"}

    def get_context_data(self, object_list=None, *args, **kwargs):
        context = super().get_context_data(object_list=object_list, *args, **kwargs)
        context["search_form"] = DateRangeForm(
            initial={"start_date": now(), "end_date": now() + timedelta(days=14)}
        )
        query = self.request.GET
        if query:
            context["query"] = ' '.join(query.values())
        return context
    
    def get_queryset(self):
        query = self.request.GET

        if query:
            start_date = f"{query.get('start_date_month')}-{query.get('start_date_day')}-{query.get('start_date_year')}"
            end_date = f"{query.get('end_date_month')}-{query.get('end_date_day')}-{query.get('end_date_year')}"

            return WorkDay.objects.filter(
                work_date__gte=datetime.strptime(start_date, "%m-%d-%Y"),
                work_date__lte=datetime.strptime(end_date, "%m-%d-%Y")
            )
        else:
            return WorkDay.objects.filter(work_date=now())
    
    def test_func(self):
        return self.request.user.is_superuser