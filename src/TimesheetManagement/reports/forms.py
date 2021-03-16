from django import forms
from django.utils.timezone import now

class DateRangeForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=tuple(range(2021, now().year + 2)))
    )
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(years=tuple(range(2021, now().year + 2)))
    )