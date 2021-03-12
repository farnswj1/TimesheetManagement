from django.db import models
from django.core.validators import RegexValidator


class WorkDay(models.Model):
    work_date = models.DateField()     
    time_in = models.TimeField()
    time_out = models.TimeField()
    hours_code = models.CharField(max_length = 4)
    fbp_payroll = models.DecimalField( max_digits = 9, decimal_places = 2) 
    amco_payroll = models.DecimalField( max_digits = 9, decimal_places = 2) 
    employee_id = models.ForeignKey()
    location_id = models.ForeignKey()
    location = models.CharField(max_length=30)
    sector = models.CharField(max_length=4)
    def hours_worked(self):
        return self.time_out - self.time_in 