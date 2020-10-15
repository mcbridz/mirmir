from django.db import models
from django.contrib.auth.models import User


class StatusField(models.Model):
    status = models.CharField(max_length=50)
    pretty_status = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.pretty_status


class SortField(models.Model):
    name = models.CharField(max_length=50)
    pretty_name = models.CharField(max_length=50)

    def __str__(self):
        return self.pretty_name


class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state_code = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=50, blank=True, null=True)
    main_phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=100)
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    birthday = models.DateField()
    status = models.ForeignKey(
        StatusField, on_delete=models.PROTECT, related_name='profile', null=True, blank=True)

    def __str__(self):
        return self.last_name + ', ' + self.first_name
