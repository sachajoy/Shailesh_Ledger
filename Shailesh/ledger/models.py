from django.db import models
import datetime
from django.shortcuts import reverse
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

    class Meta:
        ordering = ['booking_date']


    def __str__(self):
        return "{} - {}".format(self.client, self.date)

    def get_absolute_url(self):
        return reverse('add-trancation')