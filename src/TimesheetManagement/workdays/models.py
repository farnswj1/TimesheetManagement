from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.urls import reverse
from locations.models import Location
from datetime import date, time, datetime, timedelta


HOUR_CODES = (("FBP", "FBP"), ("AMCO", "AMCO"))

class WorkDay(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    work_date = models.DateField(null=False, default=now)
    time_in = models.TimeField(null=False, default=time(hour=8))
    time_out = models.TimeField(null=False, default=time(hour=16))
    hours_code = models.CharField(
        null=False, 
        max_length=4, 
        choices=HOUR_CODES,
        validators=[
            RegexValidator(
                regex="^(FBP|AMCO)$",
                message="Please choose either FBP or AMCO."
            )
        ]
    )
    fbp_payroll = models.DecimalField(
        max_digits=9, 
        decimal_places=2, 
        null=False, 
        default=0,
        validators=[
            MinValueValidator(
                limit_value=0, 
                message="Please insert a non-negative number."
            ),
            MaxValueValidator(
                limit_value=9999999.99, 
                message="Payroll must be under $10 million."
            )
        ]
    )
    amco_payroll = models.DecimalField(
        max_digits=9, 
        decimal_places=2, 
        null=False, 
        default=0,
        validators=[
            MinValueValidator(
                limit_value=0, 
                message="Please insert a non-negative number."
            ),
            MaxValueValidator(
                limit_value=9999999.99, 
                message="Payroll must be under $10 million."
            )
        ]
    )
    date_created = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return f"{self.user.full_name()}: {self.work_date} ({self.time_in}-{self.time_out})"

    def hours_worked(self):
        date_ = date(1, 1, 1)
        datetime1 = datetime.combine(date_, self.time_in)
        datetime2 = datetime.combine(date_, self.time_out)
        return datetime2 - datetime1
    
    def is_locked(self):
        return now() > self.date_created + timedelta(days=45)
    
    def get_absolute_url(self):
        return reverse("workdays:list")