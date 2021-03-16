from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.timezone import now

US_STATES = (
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DC', 'District of Columbia'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
)

# Create your models here.
def full_name(self):
    return f"{self.first_name} {self.last_name}"

User.add_to_class("full_name", full_name)


class Profile(models.Model):
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE)
    ssn = models.CharField(
        primary_key=True,
        max_length=11,
        validators=[
            RegexValidator(
                regex="^\d{3}-\d{2}-\d{4}$",
                message="Please enter a valid phone number. (XXX-XXX-XXXX)"
            )
        ]
    )
    description = models.CharField(
        max_length=30,
        null=False,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z\. ]+$",
                message="Description must consist of only letters."
            )
        ]
    )
    phone_number = models.CharField(
        max_length=12,
        null=False, 
        validators=[
            RegexValidator(
                regex="^\d{3}-\d{3}-\d{4}(-\d{2,6})?$",
                message="Please enter a valid phone number. (XXX-XXX-XXXX)"
            )
        ]
    )
    date_of_birth = models.DateField(null=False)
    address = models.CharField(
        max_length=40,
        null=False,
        validators=[
            RegexValidator(
                regex="^\d{1,5} [a-zA-Z0-9\. ]+$",
                message="Please enter a valid street address."
            )
        ]
    )
    city = models.CharField(
        max_length=25,
        null=False,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z\. -]+$",
                message="Please enter a valid city name."
            )
        ]
    )
    state = models.CharField(
        max_length=20,
        null=False,  
        choices=US_STATES
    )
    zip_code = models.CharField(
        max_length=10,
        null=False, 
        validators=[
            RegexValidator(
                regex="^\d{5}(-\d{4})?$",
                message="Please enter a valid ZIP code."
            )
        ]
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.username})"
    
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['user']