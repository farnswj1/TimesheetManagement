from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse
from django.utils.timezone import now
from datetime import timedelta

SECTORS = (("E", "East"), ("W", "West"))

# Create your models here.
class Location(models.Model):
    name = models.CharField(
        unique=True,
        max_length=30, 
        null=False,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z0-9,\. :-]+$",
                message="Please insert a valid location name."
            )
        ]
    )
    sector = models.CharField(
        max_length=1, 
        null=False, 
        choices=SECTORS,
        validators=[
            RegexValidator(
                regex="^[EW]$",
                message="Please insert either E (East) or W (West)."
            )
        ]
    )
    date_created = models.DateTimeField(null=False, default=now)

    def __str__(self):
        return f"{self.name} ({self.sector})"

    def is_locked(self):
        return now() > self.date_created + timedelta(days=45)

    def get_absolute_url(self):
        return reverse("locations:list")