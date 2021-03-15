import csv
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from workdays.models import WorkDay
from django.utils.timezone import now

# Create your views here.
def export(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)

    writer.writerow(['first_name', 'last_name', 'phone_number', 'country'])
    writer.writerow(['Huzaif', 'Sayyed', '+919954465169', 'India'])
    writer.writerow(['Adil', 'Shaikh', '+91545454169', 'India'])
    writer.writerow(['Ahtesham', 'Shah', '+917554554169', 'India'])

    return response


class Report(LoginRequiredMixin, ListView):
    model = WorkDay
    template_name = "reports/report.html"

    def get_queryset(self):
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")

        if start_date and end_date:
            pass
        else:
            return WorkDay.objects.filter(work_date=now())
    