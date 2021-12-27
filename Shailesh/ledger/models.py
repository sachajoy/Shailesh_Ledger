from django.db import models
import datetime
from django.db.models.base import Model
from django.shortcuts import reverse

class Firm(models.Model):
    name = models.CharField(unique=True, null=False, max_length=255)
    abs = models.CharField(null=False, max_length=255, unique=True)

    def get_absolute_url(self):
        return  reverse('client-list')

    def __str__(self):
        return "{}".format(self.abs)


class Client(models.Model):
    name = models.CharField(null=False, max_length=255, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return "{}, {}".format(self.name)


class Trancation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    sector = models.CharField(null=False, max_length=100)
    amount = models.IntegerField(null=False)
    remarks = models.TextField(null=True, blank=True)
    date = models.TextField()
    booking_date = models.DateField()
    passenger_list = models.TextField(null=True)
    verifed = models.BooleanField(default=False)
    cleared = models.BooleanField(default=False)
    firm = models.ForeignKey(Firm, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ['booking_date']


    def __str__(self):
        return "{} - {}".format(self.client, self.date)

    def get_absolute_url(self):
        return reverse('add-trancation')


class DateSelector(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()

    def get_absolute_url(self):
        return reverse('create-date')



