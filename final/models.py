from django.db import models

TYPE_CHOICES = (
    ('School', 'School'),
    ('Job', 'Job'),
    ('Other', 'Other')
)

class Property(models.Model):
    user = models.CharField(max_length=20)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    rent = models.CharField(max_length=100)
    bedrooms = models.CharField(max_length=2)
    bathrooms = models.CharField(max_length=2)
    link = models.CharField(max_length=200)
    notes = models.CharField(max_length=500)

class Place(models.Model):
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    user = models.CharField(max_length=20)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    notes = models.CharField(max_length=500)