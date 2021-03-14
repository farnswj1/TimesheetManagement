from django import forms
from .models import WorkDay

class WorkDayForm(forms.ModelForm):
    work_date = forms.DateField(widget=forms.SelectDateWidget())
    time_in = forms.TimeField(widget=forms.TimeInput())
    time_out = forms.TimeField(widget=forms.TimeInput())

    class Meta:
        model = WorkDay
        fields = "__all__"