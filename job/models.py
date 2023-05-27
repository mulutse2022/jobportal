from datetime import *
from django.db import models
from django.contrib.auth.models import User

import geocoder
import os

from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.


class JobType(models.TextChoices):
    PERMANENT = "PERMANENT"
    TEMPORARY = "TEMPORARY"
    INTERNSHIP = "INTERNSHIP"


class Qualification(models.TextChoices):
    PHD = "PHD"
    MASTERS = "MASTERS"
    BACHELORS = "BACHELORS"
    DIPLOMA = "DIPLOMA"
    TECHNIQUE = "TECHNIQUE/TVET"
    HIGHSCHOOL = "HIGH-SCHOOL"


class Industry(models.TextChoices):
    ADMINISTRATION = "Administration"
    BUSINESS = "Business"
    IT = "Information Technology"
    FINANCE = "Banking"
    INSURANCE = "Insurance"
    MEDIA = "Media & Journalism"
    AGRICULTURE = "Agriculture"
    ART = "Art & Design"
    MECHANIC = "Mechanic"
    CONSTRUCTION = "Construction"
    ARCHITECTURE = "Architecture"
    CUSTOMERSERVICE = "Customer Service"
    EDUCATION = "Education & Training"
    ECONOMICS = "Economics"
    ENGINEERING = "Engineering"
    ENVIRONMENT = "Natural Resource"
    HEALTHCARE = "Healthcare"
    EVENTORGANIZING = "Event Organizing"
    HOTEL = "Hotel & Hospitality"
    HR = "Human Resource"
    TELECOM = "Telecom"
    LANGUAGE = "Language"
    LEGAL = "Legal"
    LOGISTICS = "Transportation & Logistics"
    MANUFACTURING = "Manufacturing"
    MANAGEMENT = "Management"
    NGO = "NGO"
    PROJECT = "Project Management"
    PHARMACEUTICAL = "Pharmaceutical"
    MARKETING = "Marketing"
    SECURITY = "Security"
    PROCURMENT = "Procurment"
    TOURISM = "Travel & Tourism"


class Experience(models.TextChoices):
    NO_EXPERIENCE = "No Experience"
    ONE_YEAR = "1 Year"
    TWO_YEAR = "2 Years"
    THREE_YEAR = "3 Years"
    FOUR_YEAR = "4 Years"
    FIVE_YEAR = "5 Years"
    MORE_THAN_FIVE_YEARS = "Above 5 Years"


def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)


class Job(models.Model):
    title = models.CharField(max_length=250, null=True)
    description = models.TextField(null=True)
    duties_resposnsibilities = models.TextField(null=True)
    # email = models.EmailField(null=True)
    address = models.CharField(max_length=200, null=True)
    jobType = models.CharField(
        max_length=20, choices=JobType.choices, default=JobType.PERMANENT
    )
    qualification = models.CharField(
        max_length=20, choices=Qualification.choices, default=Qualification.BACHELORS
    )
    industry = models.CharField(
        max_length=30, choices=Industry.choices, default=Industry.BUSINESS
    )
    experience = models.CharField(
        max_length=20, choices=Experience.choices, default=Experience.NO_EXPERIENCE
    )
    salary = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(1000000)]
    )
    positions = models.IntegerField(default=1)
    company = models.CharField(max_length=100, null=True)
    point = gismodels.PointField(default=Point(0.0, 0.0))
    lastDate = models.DateTimeField(default=return_date_time)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    howtoapply = models.TextField(null=True)

    def save(self, *args, **kwargs):
        g = geocoder.mapquest(self.address, key=os.environ.get("GEOCODER_API"))

        print(g)

        lng = g.lng
        lat = g.lat

        self.point = Point(lng, lat)
        super(Job, self).save(*args, **kwargs)
